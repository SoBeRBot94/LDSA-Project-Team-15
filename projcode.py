from pyspark.sql import SparkSession
import re
spark_session = SparkSession.builder.master("spark://192.168.1.12:7077").getOrCreate()
#only keep emails that have the following fields and ignore the others
p1 = re.compile('MESSAGE-ID:', re.IGNORECASE)
p2 = re.compile('Subject:', re.IGNORECASE)
p3 = re.compile('Date:', re.IGNORECASE)

spark_context = spark_session.sparkContext
#read a set of emails
rdd_all = spark_context.wholeTextFiles('/home/ubuntu/DATA/enron_mail_20110402/maildir/lokey-t/inbox/1*').cache()
def f1(l):
    m= ""
    s= ""
    d= ""
    for v in l:
        if v.startswith("Message-ID:"):
            m=v
        elif v.startswith("Subject:"):
            s=v
        elif v.startswith("Date"):
            d=v
    return [m,s,d]

#get subjects and date from distinct emails
[list(v) for v in rdd_all.filter(lambda doc: bool(p1.search(doc[1])) & bool(p2.search(doc[1])) & bool(p3.search(doc[1]))).map(lambda filename_content: filename_content[1].split('\r\n\r\n')[0]).map(lambda x: x.split('\r\n')).map(f1).groupBy(lambda x:x[0]).values().take(3)]

from pyspark.sql import SparkSession

import re
spark_session = SparkSession.builder.master("spark://192.168.1.12:7077").getOrCreate()
#only keep emails that have the following fields
p1 = re.compile('MESSAGE-ID:', re.IGNORECASE)
p2 = re.compile('Subject:', re.IGNORECASE)
p3 = re.compile('Date:', re.IGNORECASE)

spark_context = spark_session.sparkContext
#read a set of emails
rdd_all = spark_context.wholeTextFiles('/home/ubuntu/DATA/enron_mail_20110402/maildir/lokey-t/inbox/1*').cache()
def f1(l):
    m= ""
    s= ""
    d= ""
    for v in l:	
		if v.startswith("Message-ID:"):
			m=v
		elif v.startswith("Subject:"):
			s=v
		elif v.startswith("Date"):
			d=v
	return [m,s,d]
	
	

spark_context.stop()
#get subjects and date from distinct emails
[list(v) for v in rdd_all.filter(lambda doc: bool(p1.search(doc[1])) & bool(p2.search(doc[1])) & bool(p3.search(doc[1]))).map(lambda filename_content: filename_content[1].split('\r\n\r\n')[0]).map(lambda x: x.split('\r\n')).map(f1).groupBy(lambda x:x[0]).values().take(3)]

#sample output
'''[[['Message-ID: <23312630.1075858967836.JavaMail.evans@thyme>', 'Subject: *EMCA* Corrected address on  Maps for the Garage Sale Saturday', 'Date: Sat, 27 Oct 2001 00:19:38 -0700 (PDT)']], [['Message-ID: <1198843.1075858972769.JavaMail.evans@thyme>', 'Subject: RE: SoCal Needles - Marketing Strategy  for Incremental Delivery', 'Date: Thu, 4 Oct 2001 14:12:52 -0700 (PDT)']], [['Message-ID: <477104.1075858970899.JavaMail.evans@thyme>', 'Subject: Levelized Sun Devil Rates', 'Date: Wed, 17 Oct 2001 07:34:34 -0700 (PDT)']]]
#TO DO:find most frequent subjects/topics in relation to Date to identify trends in emails
'''
:1,$d

spark_context.stop()