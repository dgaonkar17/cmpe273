import re
import nltk
import database
from nltk.corpus import stopwords
from nltk.tokenize import PunktSentenceTokenizer
from nltk.tokenize import word_tokenize, sent_tokenize

class Demo:
    def __init__(self, conn):
         self.conn =conn


    def processData(self,input_msg):
        stop_words = set(stopwords.words("english"))
        tokenized_msg = word_tokenize(input_msg)
        tagged = nltk.pos_tag(tokenized_msg)
        ques = []

        for k in tokenized_msg:
            if k not in stop_words:
                ques.append(k)
        return ques


    def run(self):
         exmple = "I want to book 2 deluxe rooms."
         booking_words=self.processData(exmple)
         if(any(x in booking_words for x in ['deluxe','basic','premium','book','booking']) and bool(re.search(r'\d+', exmple))):
            print(any(x in booking_words for x in ['deluxe','basic','premium','book','booking']))
            print(database.storeSentResponse(self.conn))

         question="my booking id is 123"
         list_words=self.processData(question)
         if (any(x in list_words for x in ['bookingid', 'id', 'booking']) and bool(re.search(r'\d+', question))):
            print(database.getAllResponses(self.conn))


if __name__=='__main__':
    conn=database.connectToDB()
    demo=Demo(conn)
    demo.run()