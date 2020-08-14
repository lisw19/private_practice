# TIME_COLUMN 待统计表格中所有的时间字段
TIME_COLUMN = ['CDE Undertake Date', 'CFDA Status Start Date', 'CDE Undertake Date',
               'CFDA Status Start Date', 'Review the conclusion date', 'First received Date', 'First enrolment date',
               'Study Completion Date', 'Registrated date', 'Start date', 'Registrated date',
               'Approval Date', 'Registration date', u'承办日期', u'进入补充任务最新时间', u'NMPA办理状态开始时间',
               u'首次公示日期', u'CDE承办日期', u'审评结论日期', u'首次公示信息日期', u'第一例入组日期', u'试验终止日期', u'数据最新变化日期',
               'Estimated completion date', 'Estimated start date', '审评结论时间', '最新CDE发送通知时间', '中标时间',
               'NMPA Status Start Date',
               '离开新报任务时间', '进入新报任务时间']

# NEW_TIME_COLUMN 需要标注为New的时间字段
NEW_TIME_COLUMN = ['CDE Undertake Date', 'CDE Undertake Date', 'First received Date', 'Registrated date',
                   'Registrated date', 'Approval Date', 'Registration date', u'承办日期',
                   u'CDE承办日期', u'首次公示日期', u'首次公示信息日期']

# LONG_COLUMN 特殊字段的列宽设置；默认行高30，列宽20
LONG_COLUMN = {'TA': 10,
               'Class/Target AZ Brand': 10,
               'Registration Cat.': 10,
               'Application No.': 15,
               'Review the conclusion date': 15,
               'Conclusion': 15,
               'Std. Company Name': 25,
               'Company Name': 25}

# 默克统计模块，根据id去重统计，或者更具成分词统计
ID_COLUMN = ['Approval / Registration No', 'Application No', 'Registration ID', 'Application No.']
REGISTRSTION = {'Class': ['Class', 'Class/Target AZ Brand'],
                'Related Molecular CH': ['Related Molecular CH', u'匹配库内中文成分词']