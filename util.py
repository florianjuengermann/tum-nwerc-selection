def fixWidth(width, s):
	return ("{:^"+str(width)+"}").format(s)

class Table:
	def __init__(self, withHead=True, withRowHead=True):
		self.withHead = withHead
		self.withRowHead = withRowHead
		self.rhTitle = ""
		self.th = []
		self.rh = []
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
		self.rhWidth = max(self.rhWidth, len(rhTitle))
		self.colCount= max(self.colCount, len(th))

	def addRow(self, rh:str, rData:list):
		self.rh.append(rh)
		self.data.append(rData)
		cW = max([len(x) for x in rData])
		self.cellWidth = max(self.cellWidth, cW)
		self.rhWidth = max(self.rhWidth, len(rh))
		self.colCount= max(self.colCount, len(rData))

	def toStr(self, width=120):
		tableW = 0
		colC = 0
		rhNewRow = self.rhWidth >= width/2
		if rhNewRow: 	# row-title in new row
			colC = (width-1) // (self.cellWidth+1)
			colC = min(colC, self.colCount)
			tableW = max(self.rhWidth+2, colC * (self.cellWidth+1)+1)
		else:
			colC = (width-(self.rhWidth+1)-1) // (self.cellWidth+1)
			colC = min(colC, self.colCount)
			tableW = self.rhWidth+1 + colC * (self.cellWidth+1)+1

		lines = []
		lines.append(self.horzDiv(rhNewRow, tableW, colC))
		if self.withHead:
			lines.append(self.getRow(rhNewRow, tableW, colC, self.rhTitle, self.th))
			lines.append(self.horzDiv(rhNewRow, tableW, colC))
		# data:
		for i in range(len(self.data)):
			lines.append(self.getRow(rhNewRow, tableW, colC, self.rh[i], self.data[i]))
			lines.append(self.horzDiv(rhNewRow, tableW, colC))

		return "".join(lines)

	def getRow(self, rhNewRow, tableW, colC, title, data):
		data += [''] * (self.colCount - len(data))
		line = ""
		index = 0
		if rhNewRow:
			line += "|"+fixWidth(tableW-2, title) + "|\n"			
		else:
			line += "|"+fixWidth(self.rhWidth, title)
			index = 1 + self.rhWidth
		for c in data:
			spaceLeft = tableW - index - 1
			if index == 0 and not rhNewRow:
				line += "|" + " "*self.rhWidth
				index = 1 + self.rhWidth
			if spaceLeft < 2*(self.cellWidth+1): 
				# fill row and start new
				line += "|" + fixWidth(spaceLeft-1, c) + "|\n"
				index = 0
			else:
				line += "|" + fixWidth(self.cellWidth, c)
				index += 1 + self.cellWidth
		if index != 0:
			line += " "*(tableW-1 - index) + "|\n"
		return line
	

	def horzDiv(self, rhNewRow, tableW, colC):
		s = ""
		if not rhNewRow and self.withRowHead:
			s += "+"
			s += "-"*self.rhWidth
		s += ("+" + "-"*self.cellWidth)*colC
		s += "-"* ((tableW-1)-len(s))
		s +="+\n"
		return s
