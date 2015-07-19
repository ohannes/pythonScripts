import os, sys, datetime

def getConnectionCmd(uname, ip, pwd="unknown"):
	cmd = "ssh " + uname + "@" + ip
	return cmd

def getDateToday():
	today = datetime.date.today()
	date_today = str(today.year) + "_" + str(today.month) + "_" + str(today.day)
	return date_today

def getDumpFileName(dbname):
	dump_file_name = dbname + "_" + getDateToday() + ".sql"
	return dump_file_name

def getDumpCmd(database_name, additional_options):
	cmd = "mysqldump " + database_name + " > " + getDumpFileName(dbname) + " " + additional_options
	return cmd

def getRetrCmd(uname, ip, file_path):
	cmd = "scp " + uname + "@" + ip + ":" + file_path
	return cmd

def getRakeCmd(action):
	cmd = "bundle exec rake " + action
	return cmd

def getDropCmd():
	return getRakeCmd("db:drop")

def getCrteCmd():
	return getRakeCmd("db:create")

def getMigrCmd():
	return getRakeCmd("db:migrate")

def getRestCmd(pwd, dbname, file_name):
	cmd = "mysql -u root -p" + pwd + " " + dbname + " < " + file_name
	return cmd

def getTableFileName(dbname, tname):
	file_name = dbname + getDateToday() + "_" + tname + ".csv"
	return file_name

def getExpoCmd(dbname, tname):
	cmd = "SELECT * INTO OUTFILE " + "'" + getTableFileName(dbname, tname) + "'" + " ENCLOSED BY ''	ESCAPED BY '' LINES TERMINATED BY '\n' FROM " + tname
	return cmd

def getCopyCmd(source, destination):
	cmd = "scp " + source + " " + destination
	return cmd

def getMdrpCmd(dbname):
	cmd = "mongo\n"
	cmd += "use " + dbname + "\n"
	cmd += "db.dropDatabase()"
	return cmd

def getMrtrCmd(dbname, cname, fname):
	cmd = "mongoimport --type csv --db " + dbname + " --collection " + cname + " --file " + fname + " --headerline"
	return cmd

def getIndxCmd(dbname, cname, fields):
	cmd = "mongo\n"
	cmd += "use " + dbname + "\n"
	cmd += "db." + cname + ".ensureIndex("
	i = 0
	for field in fields:
		cmd += "{" + field + ":" + "1" + "}"
		if i != len(fields) - 1:
			cmd += ","
		i += 1
	cmd += ")"

def getUnixTimeStr(year, month, day):
	t = datetime.datetime(year, month, day, 0, 0, 0, 0)
	t_str = str(t.strftime("%s"))
	return t_str

def getStartTime():
	today = datetime.date.today()
	start_time = getUnixTimeStr(today.year, today.month - 1, 1)
	return start_time

def getEndTime():
	today = datetime.date.today()
	end_time = getUnixTimeStr(today.year, today.month, 1)
	return end_time

def getRprtCmd(mdname, mtname, params):
	cmd = "rails c\n"
	cmd += mdname + "." + mtname + "("
	i = 0
	for param in params:
		cmd += param
		if i != len(params) - 1:
			cmd += ", "
		i += 1
	cmd += ")"
	return cmd

uname = "artkn"
ip = "10.106.231.24"
pwd = "arcelik123"
dbname = "appstore_production"
add_opts = "--ignore-table=appstore_production.zapping_usages"
file_path = "/home/artkn/" + getDumpFileName(dbname)
local_pwd = ""
local_dbname = "server_development"
dump_path = "/home/artkn/mongo_dumps"
change_table = {}
m_dbname = "statistics"

conn_cmd = getConnectionCmd(uname, ip, pwd)
dump_cmd = getDumpCmd(dbname, add_opts)
retr_cmd = getRetrCmd(uname, ip, file_path)
drop_cmd = getDropCmd()
crte_cmd = getCrteCmd()
rest_cmd = getRestCmd(local_pwd, local_dbname, getDumpFileName(dbname))
migr_cmd = getMigrCmd()
ausg_cmd = getExpoCmd(local_dbname, "application_usages")
cusg_cmd = getExpoCmd(local_dbname, "channel_usages")
ccpy_cmd = getCopyCmd(getTableFileName(local_dbname, "application_usages"), dump_path)
acpy_cmd = getCopyCmd(getTableFileName(local_dbname, "channel_usages"), uname + "@" + ip + ":" + dump_path)
#arnm_cmd = getRnmeCmd("application_usages", change_table)
#arnm_cmd = getRnmeCmd("channel_usages", change_table)
mdrp_cmd = getMdrpCmd(m_dbname)
amrt_cmd = getMrtrCmd(m_dbname, "application_usages", getTableFileName(local_dbname, "application_usages"))
cmrt_cmd = getMrtrCmd(m_dbname, "channel_usages", getTableFileName(local_dbname, "channel_usages"))
andx_cmd = getIndxCmd(m_dbname, "application_usages", ["device_id", "background"])
cndx_cmd = getIndxCmd(m_dbname, "channel_usages", ["device_id", "background"])
rprt_cmd = getRprtCmd("UsageStatistic", "generate_report_pdf", [getStartTime(), getEndTime(), "Monthly"])