
import sqlite3




conn = sqlite3.connect('database.db')
c = conn.cursor()

#Set Up 
def setupDB():
    c.execute('''CREATE TABLE IF NOT EXISTS Users
             (name varchar(20) NOT NULL, email varchar(20), id int, PRIMARY KEY (name))''')
    c.execute('''CREATE TABLE IF NOT EXISTS Debts
             (name FORIEGN KEY REFERENCES Users(name), id FORIEGN KEY REFERENCES Users(id), zero decimal(10,2), one decimal(10,2), two decimal(10,2), three decimal(10,2), four decimal(10,2), five decimal(10,2), PRIMARY KEY (name))''')



def intToWord(num):
    if num ==0:
        return 'zero'
    if num ==1:
        return 'one'
    if num ==2:
        return 'two'
    if num ==3:
        return 'three'
    if num ==4:
        return 'four'
    if num ==5:
        return 'five'
    


def addUser(name,email):
    c.execute('''SELECT name FROM Users WHERE name = '{name}' ''')
    
    #get counter 
    c.execute('''SELECT Count(*) FROM Users ''')
    buffer = c.fetchone()
    counter = buffer[0]
    
    c.execute(f'''SELECT * FROM Users WHERE name = '{name}' ''')
    buffer = c.fetchone()
    nameUsed=buffer[0]
    
    if counter >=6 :
        print('Group is full')
    
    elif nameUsed != None:
        print('Name already taken')
    else:
        c.execute(f'''INSERT INTO USERS VALUES ('{name}','{email}',{counter})''')
        c.execute(f'''INSERT INTO DEBTS VALUES ('{name}',{counter},0,0,0,0,0,0)''')
        print("name inserted")
        conn.commit()

def deleteUser(name):
    c.execute(f'''SELECT name FROM Users WHERE name = '{name}' ''')
    
    if c.fetchone() != None:
        c.execute(f'''DELETE FROM Debts WHERE name = '{name}' ''')
        c.execute(f'''DELETE FROM Users WHERE name = '{name}' ''')
        print('user deleted')
        conn.commit()
    else:
        print('user doesnt exist')

def addDebts(borrower,lender,amount):
    
    c.execute(f'''SELECT name FROM Users WHERE name = '{borrower}' OR name ='{lender}' ''')
    
    if amount <0.0:
        print('must be a positive value')
    elif len(c.fetchall())!= 2:
        print('one name not found ')
    else:
        c.execute(f'''SELECT id FROM Users WHERE name = '{lender}' ''')
        id = intToWord(c.fetchone()[0])
       
        c.execute(f'''SELECT {id} FROM Debts WHERE name = '{borrower}' ''')
        current= float(c.fetchone()[0])
       
        c.execute(f'''UPDATE Debts SET {id} = {amount+current} WHERE name='{borrower}' ''')
        print(f'{borrower} now owes {lender} an additional {amount} ')
        conn.commit()
        
def makePayment(borrower,lender,amount):
    c.execute(f'''SELECT name FROM Users WHERE name = '{borrower}' OR name ='{lender}' ''')
    if len(c.fetchall())!= 2:
        print('one name not found ')
    else:
        c.execute(f'''SELECT id FROM Users WHERE name = '{lender}' ''')
        id = intToWord(c.fetchone()[0])
        c.execute(f'''SELECT {id} FROM Debts WHERE name = '{borrower}' ''')
        balance = float(c.fetchone()[0])
        if amount>balance:
            print('payment can not be greater than amount owed')
        else:
            c.execute(f'''UPDATE Debts SET {id} = {balance-amount} WHERE name='{borrower}' ''')
            print("payment recorded")
            conn.commit()

#row one is my id            
def individualDebts(name): 

    c.execute(f'''SELECT id, zero, one, two, three, four, five FROM Debts WHERE name = '{name}' ''')
    debts = c.fetchone()
    return debts
    #row one is my id

def sumDebts(name):
    c.execute(f'''SELECT zero, one, two, three, four, five FROM Debts WHERE name = '{name}' ''')
    debts = c.fetchone()
    sum=0
    for x in debts:
        sum+=float(x)
    return sum

def printAll():
    c.execute(f'''SELECT id, zero, one, two, three, four, five FROM Debts ''')
    debts = c.fetchall()
    
    sumDebts=[0.0]*6
    for user in debts:
        sum=0
        for x in range(1, len(user)):
            sum+= float(user[x])
        #gets id number 
        sumDebts[int(user[0])]=sum
    return sumDebts  

def mapUsers():
    c.execute('''SELECT name, id FROM Users ''')
    array=c.fetchall()
    return array

def numUsers():
    c.execute('''SELECT Count(*) FROM Users ''')
    buffer = c.fetchone()
    return int(buffer[0])










    
    
