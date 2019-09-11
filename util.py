import json
from pytz import timezone

def readConfig():
  with open('config.json') as f:
    return json.load(f)
  return {}

def readChatIds():
	try:
		with open('chatIds.json') as f:
			return json.load(f)
	except:
		pass
	return []

def saveChatIds(ids:list):
	with open("chatIds.json", "w") as f:
		json.dump(ids, f)

def convertTimeZone(date, fromTimeZone, toTimeZone):
	fromTZ = timezone(fromTimeZone)
	date = fromTZ.localize(date)
	return date.astimezone(timezone(toTimeZone))


def fixWidth(width, s):
	return ("{:^"+str(width)+"}").format(s)
def fixWidthR(width, s):
	return ("{:"+str(width)+"}").format(s)
def fixWidthL(width, s):
	return ("{:<"+str(width)+"}").format(s)


class Table:
	def __init__(self, withHead=True, withRowHead=True, displayKey = True):
		self.withHead = withHead
		self.withRowHead = withRowHead
		self.displayKey = displayKey
		self.rhTitle = ""
		self.th = []
		self.rh = []
		self.rKey = [] # key for each row. Used for sorting
		self.data = [] # 2D
		# widths:
		self.rhWidth = 0
		self.cellWidth = 0 # inner cells
		self.colCount = 0
	
	def setHead(self, th):
		self.th = th

	def setHead(self, rhTitle, th):
		self.rhTitle = rhTitle
		self.th = th
		self.setMaxValues(rhTitle, th)

	def addRow(self, rh:str, rData:list, key:float = None):
		self.rh.append(rh)
		self.rKey.append(key)
		self.data.append(rData)
		self.setMaxValues(rh, rData)

	def setMaxValues(self, title:str, data:list):
		cW = max([len(x) for x in data])
		self.cellWidth = max(self.cellWidth, cW)
		self.rhWidth = max(self.rhWidth, len(title))
		self.colCount= max(self.colCount, len(data))

	def toStr(self, width=120):
		if self.displayKey:
			rhWidth = self.rhWidth + len(":99.99") + len("10. ")
		tableW = 0
		colC = 0
		print("width:", width, "rhWidth", rhWidth)
		rhNewRow = rhWidth >= width/2
		if rhNewRow: 	# row-title in new row
			colC = (width-1) // (self.cellWidth+1)
			colC = min(colC, self.colCount)
			tableW = max(rhWidth+2, colC * (self.cellWidth+1)+1)
		else:
			colC = (width-(rhWidth+1)-1) // (self.cellWidth+1)
			colC = min(colC, self.colCount)
			tableW = rhWidth+1 + colC * (self.cellWidth+1)+1

		lines = []
		lines.append(self.horzDiv(rhNewRow, rhWidth, tableW, colC))
		if self.withHead:
			lines.append(self.getRow(rhNewRow, rhWidth, tableW, colC, self.rhTitle, None, self.th))
			lines.append(self.horzDiv(rhNewRow, rhWidth, tableW, colC))
		# data:
		rank = 1
		for i in range(len(self.data)):
			if i > 0 and self.rKey[i-1] != self.rKey[i]:
				rank = i+1
			lines.append(self.getRow(rhNewRow, rhWidth, tableW, colC, 
										self.rh[i], self.rKey[i], self.data[i], rank))
			lines.append(self.horzDiv(rhNewRow, rhWidth, tableW, colC))


		return "".join(lines)

	def getRow(self, rhNewRow, rhWidth, tableW, colC, title, key, data, rank=None):
		data += [''] * (self.colCount - len(data))

		line = ""
		index = 0
		if self.displayKey and key != None:
			keyStr = "{:5.2f}".format(key)
			title = title + ":"
		else:
			keyStr = ""

		if rank != None:
			title = fixWidthR(2, rank)+". " + title

		if rhNewRow:
			title = fixWidthL(tableW-2-len(keyStr), title)
			line += "|" + title + keyStr + "|\n"
		else:
			title = fixWidthL(rhWidth-len(keyStr), title)
			line += "|" + title + keyStr
			index = 1 + rhWidth
		for c in data:
			spaceLeft = tableW - index - 1
			if index == 0 and not rhNewRow:
				line += "|" + " "*rhWidth
				index = 1 + rhWidth
			if spaceLeft < 2*(self.cellWidth+1): 
				# fill row and start new
				line += "|" + fixWidth(spaceLeft-1, c) + "|\n"
				index = 0
			else:
				line += "|" + fixWidthR(self.cellWidth, c)
				index += 1 + self.cellWidth
		if index != 0:
			line += " "*(tableW-1 - index) + "|\n"
		return line
	

	def horzDiv(self, rhNewRow, rhWidth, tableW, colC):
		s = ""
		if not rhNewRow and self.withRowHead:
			s += "+"
			s += "-"*rhWidth
		s += ("+" + "-"*self.cellWidth)*colC
		s += "-"* ((tableW-1)-len(s))
		s +="+\n"
		return s

	def sort(self, rev=True):
		self.rKey, self.rh, self.data = zip(*sorted(zip(self.rKey, self.rh, self.data), reverse=True))
