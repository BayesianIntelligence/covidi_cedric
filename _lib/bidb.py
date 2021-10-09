"""

Interface layer to the database on the Java side.

"""
from __future__ import print_function

from builtins import range
import sqlite3, re

class DB:
	def __init__(self, path):
		if hasattr(path,'execute'):
			self.conn = path
			self.conn.row_factory = sqlite3.Row
		else:
			self.conn = sqlite3.connect(path, timeout = 10)
			#self.conn = sqlite3.connect(path)
			self.conn.execute("PRAGMA busy_timeout = 1000")
			self.conn.row_factory = sqlite3.Row
		self.debug = False
	
	def __enter__(self):
		return self
	
	def __exit__(self, type, value, tb):
		self.conn.close()
	
	def query(self, sql, params = None, ignoreErrors = False, keyType = "name"):
		if keyType == "index":
			self.conn.row_factory = None
		else:
			self.conn.row_factory = sqlite3.Row
		
		if params is None: params = []
		if self.debug:
			print("query:",sql,"<br>")
			print("params:",params,"<br>")
			
		if ignoreErrors:
			rs = None
			try:
				rs = self.conn.execute(sql, params)
			except: pass
		else:
			rs = self.conn.execute(sql, params)
		
		# Always commit
		self.conn.commit()
		
		return rs
	
	def handleValType(self, val):
		return bautils.convertNumber(val)
		'''try:
			val = int(val)
		except:
			try:
				val = float(val)
			except: pass
		
		return val'''
	
	# This will be efficient, simple and protect against injections
	def intParams(self, lst):
		sqlFrag = "("
		sep = ""
		for item in lst:
			int(item) # If not int, throw error
			sqlFrag += sep + str(item)
			sep = ","
		
		sqlFrag += ")"
		
		return sqlFrag
	
	# Creates the placeholders string. More general than above function, but involves
	# duplication and is less efficient
	def placeholders(self, lst):
		return "("+("?,"*len(lst))[:-1]+")"

	def queryValue(self, sql, params = None, typeHandling = True, ignoreErrors = False):
		rs = self.query(sql, params, ignoreErrors)
		if rs is None: return None
		row = rs.fetchone()
		if row is None:  return None

		return row[0]
	
	# keyType can be "name" or "index"
	def queryRow(self, sql, params = None, keyType = "name", typeHandling = True, ignoreErrors = False):
		rs = self.query(sql, params, ignoreErrors, keyType)
		row = rs.fetchone()
		if row is None:  return None
		
		if keyType == "name":
			return dict(row)
		elif keyType == "index":
			return list(row)
	
	# keyType can be "name" or "index"
	def queryRows(self, sql, params = None, keyType = "name", typeHandling = True, oneD = False, ignoreErrors = False):
		rs = self.query(sql, params, ignoreErrors, keyType)

		if oneD:
			data = []
			for row in rs:
				data.extend(row)
			return data
		
		rows = rs.fetchall()
		if rows is None:  return None
		
		if keyType == "name":
			return [dict(r) for r in rows]
		elif keyType == "index":
			return [list(r) for r in rows]
	
	# Returns a map of field1 to field2 (which are the first and second fields, respectively, by default)
	def queryMap(self, sql, params = None, ignoreErrors = False, field1 = 0, field2 = 1):
		rs = self.query(sql, params, ignoreErrors)

		map = {}
		for row in rs:
			map[row[field1]] = row[field2]
		
		return map

	def update(self, table, upds, condition, params, ignore = []):
		if not params: params = []

		updStr = ""
		sep = ""
		i = 0
		for field,val in upds.items():
			if field in ignore:  continue
			params.insert(i, val)
			updStr += sep + field + "= ?"
			sep = ", "
			i += 1
	
		if condition:
			condition = " where "+condition
		
		sql = "update "+table+" set "+updStr+condition
		
		if self.debug:
			print("query:",sql,"<br>")
			print("params:",params,"<br>")
		
		self.query(sql, params)
	
	def replace(self, table, upds, pk):
		recordExists = self.queryValue("select 1 from {} where {} = ?".format(table, pk), [upds[pk]])
		
		if not recordExists:
			insertFields = [k for k in upds.keys() if k!=pk] if (isinstance(upds[pk],int) and upds[pk]<0) else upds.keys()
			fieldStr = ", ".join(insertFields)
			placeholdersStr = ("?,"*len(insertFields))[:-1]
			params = [upds[f] for f in insertFields]
			sql = "insert into {} ({}) values ({})".format(table, fieldStr, placeholdersStr)
			if self.debug: print(sql, params)
			self.query(sql, params)
			
			return self.queryValue("select last_insert_rowid()")
		else:
			updateFields = upds.keys()
			fieldSetStr = ", ".join(k+" = ?" for k in updateFields)
			params = [upds[f] for f in updateFields] + [upds[pk]]
			sql = "update {} set {} where {} = ?".format(table, fieldSetStr, pk)
			if self.debug: print(sql, params)
			self.query(sql, params)
			
			return upds[pk]
	
	'''
	changeSet structure should be: array(
		"changed" => array(
			<pkValue> => array("field1" => val, etc.),
			<pkValue2> etc.
		),
		"inserted" => array(
			array("field1" => val, etc.),
			array("field1" => val, etc.),
			etc.
		),
		"deleted" => array(<pkValue>, <pkValue2>, etc.)
	)
	'''
	def applyTableChanges(self, table, changeSet, pkName):
		newPkMap = {}
		
		for pk, record in changeSet["changed"].items():
			record[pkName] = int(pk)
			self.replace(table, record, pkName)

		for record in changeSet["inserted"]:
			oldPk = record[pkName]
			record[pkName] = None
			newPk = self.replace(table, record, pkName)
			newPkMap[oldPk] = newPk

		for pk in changeSet["deleted"]:
			self.query("delete from "+table+" where "+pkName+" = ?", [pk])

		return newPkMap

	def tableExists(self, table):
		return (self.queryValue("select 1 from sqlite_master where type='table' and name = ?", [table]) is not None)
		
	def fieldNames(self, rs):
		return [r[0] for r in rs.description]
	
	def writeCsv(self, inTable, outCsvFn, fields = "*", where = None):
		import csv
		with open(outCsvFn, "wb") as outCsvFile:
		
			rs = self.query("select "+",".join(fields)+" from "+inTable+((" where "+where) if where else ""))
			
			# Write headers
			if fields == "*":
				headers = self.getColumnNames(rs)
			else:
				headers = fields
			outCsv = csv.DictWriter(outCsvFile, headers)
			outCsv.writerow(dict(zip(headers,headers)))
			
			for row in rs:
				row = dict(row)
				outCsv.writerow(dict((k,row[k]) for k in headers if k in row))

			rs.close()
	





	# XXX: Everything below not yet converted




	def fetchRow(self, rs, keyType = "name", typeHandling = True, omit = None):
		md = rs.getMetaData()
		
		row = {} if keyType in ["name","both"] else []
		
		for i in range(md.getColumnCount()):
			if keyType in ["name","both"]:
				row[md.getColumnName(i+1)] = rs.getString(i+1)
			if keyType == "both":
				row[i] = rs.getString(i+1)
			elif keyType == "index":
				row.append(rs.getString(i+1))
		
		if typeHandling:
			lst = row.items() if isinstance(row,dict) else enumerate(row)
			for k,val in lst:
				row[k] = self.handleValType(val)
		
		# Remove unwanted items
		if omit:
			for omitItem in omit:
				del row[omitItem]

		return row
	
	def fetchRows(self, rs, keyType = "name", typeHandling = True, oneD = False):
		rows = []
		
		colCount = rs.getMetaData().getColumnCount()
	
		while next(rs):
			if oneD:
				for i in range(colCount):
					rows.append(rs.getString(i+1))
			else:
				rows.append(self.fetchRow(rs, keyType, typeHandling))
		
		return rows
	
	# FIX: Do
	def createIndex(self, onTable, onColumn):
		pass
	
	def copyTableStructure(self, inTable, outTable):
		#rint inTable,outTable,"{{"
		
		tableInfo = self.query("select sql from sqlite_master where type = 'table' and name = ?", [inTable])
		next(tableInfo)
		
		createTableSql = tableInfo.getString('sql')
		
		tableInfo.close()
		
		newSql = re.sub(r'create table [`\'"]?\w+[`\'"]?', 'create table '+outTable, createTableSql, flags=re.IGNORECASE)
		
		#rint newSql
		
		self.query(newSql)

		# Copy across indexes
		
		rs = self.query("select sql from sqlite_master where type = 'index' and tbl_name = ?", [inTable])
		while next(rs):
			newIndexSql = rs.getString('sql')
			newIndexSql = re.sub(r'(create(?:\s+unique)?\s+index\s+)([`\'"]?\w+[`\'"]?)(\s+on\s+)([`\'"]?\w+[`\'"]?)', r'\1bwauto_'+bautils.genPass(20)+r'\3'+outTable, newIndexSql, flags=re.IGNORECASE)
			
			self.query(newIndexSql)
		
		rs.close()
	
	def shiftTables(self, *tables, **kw):
		""" Renames table[0] to table[1], table[1] to table[2], ..., table[n] to replace. Call as
				shiftTables(table1, table2, to=table3)
		
		    Warning: This will drop the 'to' table! """
		
		if "to" in kw:
			to = kw["to"]
			
			# Make sure all the tables exist first
			rs = self.query("select count(*) as cnt from sqlite_master where type='table' and name in ('"+("','".join(tables))+"')")
			next(rs)
			count = rs.getInt("cnt")
			rs.close()
			if count!=len(tables):
				# Don't print warning if ignoreMissing set, just quit
				if not kw.get("quietFailOnMissing"):
					print("Not all the tables (ignoring 'to') exist")
				return
		
			self.query("drop table if exists "+to)

			tables = list(tables)
			tables.append(to)

			for i in range(len(tables),1,-1):
				i -= 1
				self.query("alter table "+tables[i-1]+" rename to "+tables[i])
		else:
		
			print("No 'to' keyword given to 'shiftTables'")
	
	def sqlJoin(self, joins):
		sql = joins["baseTable"]
		
		for jn in joins["joins"]:
			if jn["complexJoin"]:
				sql += jn["complexJoin"]
			else:
				fieldLeft = jn["fieldLeft"]
				fieldRight = jn["fieldRight"]
				
				if re.search(r'^[a-zA-Z0-9_]+$', fieldLeft):
					# Plain field, so add table name
					fieldLeft = jn["tableLeft"]+"."+fieldLeft
				if re.search(r'^[a-zA-Z0-9_]+$', fieldRight):
					# Plain field, so add table name
					fieldRight = jn["tableRight"]+"."+fieldRight				
				
				sql += " left join "+jn["tableRight"]+" on "+fieldLeft+" = "+fieldRight
		
		return sql
	
	# Needs to work with partial sql too (like just the join expressions)
	def changeTableInSql(self, sql, fromTable, toTable): 
		# FIX: Need to properly parse the sql join
		sql = re.sub(r'\b'+fromTable+r'\b', toTable, sql)
		return sql
	
	# Convert the rs into a dict/object in the Data/Headers format (i.e. {headers:...,data:...})
	# Note: Only works for one iteration! (The advantage is it saves memory.)
	def makeDataOnce(self, rs):
		headers = self.getColumnNames(rs)
		def getRow():
			while next(rs):
				yield self.fetchRow(rs, keyType = "index")
			rs.close()
		
		return {"headers": headers, "data": getRow()}
		
	# Convert the rs into a dict/object in the Data/Headers format (i.e. {headers:...,data:...})
	def makeData(self, rs):
		headers = self.getColumnNames(rs)
		data = self.fetchRows(rs, keyType = "index")
		rs.close()
		
		return {"headers": headers, "data": data}

