class messageKey():
    def __init__(self, sourceCode, time):
        self.m_sourceCode = sourceCode
        self.m_time = time

    def __eq__(self, other):
        return (self.m_sourceCode == other.m_sourceCode and self.m_time == other.m_time)

    def __hash__(self):
        return hash((self.m_sourceCode, self.m_time))

    def compareTime(self, other):
        retVal = None
        if self.m_sourceCode == other.m_sourceCode:
            if self.m_time < other.m_time:
                retVal =  -1
            elif self.m_time > other.m_time:
                retVal =  1
            else:
                retVal = 0
        return retVal
                