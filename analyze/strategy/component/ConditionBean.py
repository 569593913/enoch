class ConditionBean:
    """"""
    def __init__(self,group=None,buyK=None,condition=None):
        """"""
        self.group = group
        self.condition = condition
        self.buyK = buyK

    def __repr__(self):
        return 'ConditionBean:{group=%s,buyK=%s,condition=%s}' % (self.group,self.condition,self.buyK)