class messageKey():
    def __init__(self, sourceCode, time):
        self.m_sourceCode = sourceCode
        self.m_time = time

    def __eq__(self, other):
        return (self.m_sourceCode == other.m_sourceCode and self.m_time == other.m_time)