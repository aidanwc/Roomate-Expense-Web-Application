
import sqlite3




conn = sqlite3.connect('database.db',check_same_thread=False)
c = conn.cursor()

#Set Up 
def setupDB():
    c.execute('''CREATE TABLE IF NOT EXISTS Users
             (name varchar(20) UNIQUE NOT NULL, email varchar(30), PRIMARY KEY (name))''')
    c.execute('''CREATE TABLE IF NOT EXISTS Debts
             (borrower FORIEGN KEY REFERENCES Users(name), lender FORIEGN KEY REFERENCES Users(name), amount decimal(10,2), PRIMARY KEY (borrower, lender))''')




def addUser(name,email):
   
    
    #get counter 
    c.execute('''SELECT Count(*) FROM Users ''')
    buffer = c.fetchone()
    counter = buffer[0]
    
    c.execute(f'''SELECT * FROM Users WHERE name = '{name}' ''')
    nameUsed=c.fetchone()
    
    print(name)
    
    if counter >=6 :
        print('Group is full')
    
    elif nameUsed != None:
        print('Name already taken')
    else:
        c.execute(f'''INSERT INTO USERS VALUES ('{name}','{email}')''')
        print("name inserted")
        conn.commit()

def deleteUser(name):
    c.execute(f'''SELECT name FROM Users WHERE name = '{name}' ''')
    
    if c.fetchone() != None:
        c.execute(f'''DELETE FROM Debts WHERE lender = '{name}' OR borrower = '{name}' ''') #change later
        c.execute(f'''DELETE FROM Users WHERE name = '{name}' ''')
        print('user deleted')
        conn.commit()
    else:
        print('user doesnt exist')

def addDebts(borrower,lender,amount):
    try:
        amount= round(float(amount),2)
    except:
        amount=0.0
   
    c.execute(f'''SELECT name FROM Users WHERE name = '{borrower}' OR name ='{lender}' ''')
    
    if amount <0.0:
        print('must be a positive value')
    elif len(c.fetchall())!= 2:
        print('one name not found ')
    else:
      
       
        c.execute(f'''SELECT amount FROM Debts WHERE borrower = '{borrower}' AND lender = '{lender}' ''')
        buffer = c.fetchone()
        
        if buffer != None:
            current = float(buffer[0])
            c.execute(f'''UPDATE Debts SET amount = {amount+current} WHERE borrower='{borrower}' AND lender = '{lender}' ''')
        else:
            c.execute(f'''INSERT INTO Debts VALUES ('{borrower}','{lender}', {amount}) ''')
        
        print(f'{borrower} now owes {lender} an additional {amount} ')
        conn.commit()
        
def makePayment(borrower,lender,amount):
    try:
        amount= round(float(amount),2)
    except:
        amount=0.0
    
    c.execute(f'''SELECT name FROM Users WHERE name = '{borrower}' OR name ='{lender}' ''')
    if len(c.fetchall())!= 2:
        print('one name not found ')
    else:
       
        c.execute(f'''SELECT amount FROM Debts WHERE borrower = '{borrower}' AND lender = '{lender}' ''')
        
        buffer = c.fetchone()
        
        if buffer != None:
            balance = float(buffer[0])
            if amount<=balance:
                c.execute(f'''UPDATE Debts SET amount = {balance-amount} WHERE borrower='{borrower}' AND lender = '{lender}' ''')
                conn.commit()
            else:
                print('payment can not be greater than amount owed')
    
        else:
            print("No existing balance between two users")
            conn.commit()

#row one is my id            
def individualDebts(name): 

    c.execute(f'''SELECT borrower, lender, amount FROM Debts WHERE borrower = '{name}' ''')
    debts = c.fetchall()
    return debts
    

def sumDebts(name):
    c.execute(f'''SELECT amount FROM Debts WHERE borrower = '{name}' ''')
    debts = c.fetchall()
    sum=0
    for x in debts:
        sum+=float(x[0])
    return sum

def printAll():
    c.execute(f'''SELECT name FROM Users ''')
    users = c.fetchall()
    ledger=[]*numUsers()
    
    for x in users:
       sum = sumDebts(x[0])
       map = [x[0],sum]
       ledger.append(map)
       
    
    return ledger  

def numUsers():
    c.execute('''SELECT Count(*) FROM Users ''')
    buffer = c.fetchone()
    return int(buffer[0])







    
    
