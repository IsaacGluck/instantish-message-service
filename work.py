#!/usr/bin/python
print 'Content-Type: text/html\n'
print ''
import cgi,cgitb,os, sys, stat
from time import strftime, localtime
cgitb.enable()

form = cgi.FieldStorage()

r = open('registered.txt', 'r')
u = open('users.txt', 'r')
users = u.read().split('\n')
u.close()

page = ''

#Isaac - Register
def register():
    #both fields required
    if 'username' not in form or 'pswd' not in form or 'pcheck' not in form:
        return '<h1>Error. You must enter a username and password to register. <a href="web/register.html">Try Again</a></h1>'
    username = form['username'].value
    pwrd = form['pswd'].value
    pcheck = form['pcheck'].value
    #no symbols allowed allowed!
    char = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for i in username:
        if i not in char:
            return '<h1>Error. No spaces or symblos allowed. <a href="web/register.html">Try Again</a></h1>'
    #check password confirmation
    if pwrd != pcheck:
        return '<h1>Error. You did not confirm your password correctly. <a href="web/register.html">Try Again</a></h1>'
    #check username duplicates
    if username in users:
        return '<h1>Error. This username is already in use. Please select a different username <a href="web/register.html">here</a></h1>'
    a = open('registered.txt', 'a')
    b = username + ':' + form['pswd'].value + '\n'
    a.write(b)
    a.close()
    c = 'users/' + username + '.txt'
    d = open(c, 'w')
    e = username + '@@'
    d.write(e)
    d.close()
    g = open('users.txt', 'a')
    g.write(username + '\n')
    g.close()
    return '<h1>Thank you for registering, you may now login <a href="web/login.html">here</a></h1>'

#Isaac - Login
def login():
    #both fields required
    if 'username' not in form or 'pswd' not in form:
        return '<h1>Error. You must enter a username and password to login. <a href="web/login.html">Try Again</a></h1>'
    b = r.read().split('\n')
    r.close()
    username = form['username'].value
    pswd = form['pswd'].value
    #both fields must match
    if (username + ':' + pswd) not in b:
        return '<h1>Error. Username/Password combination do not match, please <a href="web/login.html">Try Again</a></h1>'
    a = '''<!DOCTYPE html>
<html>
<head>
<title>'''
    
    a += username
    
    a +='''</title>
<link type="text/css" rel="stylesheet" href="web/styles/profile.css"/>
<link rel="shortcut icon" href="web/img/favicon.ico" type="image/x-icon">
<link rel="icon" href="web/img/favicon.ico" type="image/x-icon">
</head>
<body>
<div id="header">
<span id="header1"> <h1>'''
    
    a += username
    
    a+= '''</h1> </span>
<span id="header2"> <h2><a href="web/login.html">Log Out</a></h2> </span>
</div>
<div id="chat">
<h3>Select a User to Chat With</h3>
<form name="input" action="work.py" method="post">
<select name="users">'''

    #Isaac - create a dropdown list of registered users who you can chat with
    for i in b[:-1]:
        k = i.split(':')
        if k[0] != username:
            a += '<option>' + k[0] + '</option>'
        
    a += '''</select><br>
<input type="hidden" name="username" value='''
    a += username

    a +='''><input type="submit" name="chat" value="submit">
</form>

<h3>Blocked Users:</h3>'''

    #Isaac - create a list of blocked users from a persons .txt file
    m = open( 'users/' + username + '.txt', 'r')
    p = m.read().split('@')[1]
    m.close()

#    if ',' in p:
    plist = p.split(',')
    for i in plist:
        if i != '' and i != ' ':
            a += '<p>' + i + '</p>'
#    else:
#        a += '<p>' + p + '</p>'


    a +='''</div>
<div id="already">
<h3>You are chatting with:</h3>'''



    #create a list of usernames you're already having a conversation with
    z = open('users/' + username + '.txt', 'r')
    prof = z.read().split('$')
    z.close()
    for i in prof:
        if i != username and i in users:
            chatting = i
            a += '<p>' + chatting + '</p>'
            
    a +='''</div>
<div id="notyet">
<h3>You are not chatting with:</h3>'''
    #create a list of usernames you're not chatting with yet
    for i in users:
        if i != username and i not in prof:
            notchat = i
            a += '<p>' + notchat + '</p>'

    a += '''</div><div id="block">
    <h3>Block Users:</h3>
    Add users to your block list:
    <form name="input" action="work.py" method="post">'''
    #<script language="JavaScript">
    #function selectText(textField) 
    #{
    #textField.focus();
    #textField.select();
    #}
    #</script>
    a += '<input type="text" name="who"' #value="Usernames separated by commas" onClick='selectText(this); this.onclick=null;'
    a += ''' placeholder="Usernames seperated by commas" class="long">
    <input type = "hidden" name = "username" value= '''

    a += username

    a +=''' ><br>
    <input type ="submit" name = "block" value ="Block"><br>
    </form>'''

    a += '''<h3>Unblock Users:</h3>
    Remove users to your block list:
    <form name="input" action="work.py" method="post">
    <select name="unblock">'''

    #Isaac - create a list of blocked people,  allow users to unblock people
    q = open('users/' + username + '.txt', 'r')
    unblock = q.read().split('@')[1].split(',')
    q.close()
    for i in unblock:
        if i != '' and i != ' ':
            a += '<option>' + i + '</option>'


    a+= '''</select>
    <input type = "hidden" name = "username" value="'''

    a += username

    a += '''"><br>
    <input type ="submit" name = "deblock" value ="unblock"><br>
    </form></div>'''

    a +='''
<div id="bottom">
<p>&copy; 2013 Isaac Gluck and Hubert Puszklewicz</p>
<p> Mr. Jaishankar Period 9</p>
</div>
'''
    return a
    
def conversation(u, o): #Hubert - display the conversation with certain user
    if 'username' in form and 'users' in form:
        username = form['username'].value
        other = form['users'].value
    else:
        username = u
        other = o
    a = open('users/' + username + '.txt', 'r')
    ab = a.read()
    au = ab.split('$')
    a.close()

    a1 = open('users/' + other + '.txt', 'r')
    bl = a1.read().split('@')
    checkblock = bl[1].split(',')
    a1.close()

    ownblock = ab.split('@')[1].split(',')

    
    #Stop blocked users from messaging each other 
    if username in checkblock:
        return ' <font color="red"><h1>Error. It seems that this user has blocked you. <form name="input" action="work.py" method="post"><input type="hidden" name="username" value ="' + username + '"><input type="submit" name="back" value="Go Back"></form></h1></font>'

    # Splice the read .txt file to display only the conversation
    if other in au:
        convo = au[au.index(other) + 1]
        
    #if the username that was called wasn't present in the .txt file, start a new conversation 
    else:
        convo = 'Start your conversation below.<br>'
        
    main ='<!DOCTYPE html><html><head><title>'
    main += username
    main +='</title><link type="text/css" rel="stylesheet" href="web/styleschat.css"/><link rel="shortcut icon" href="web/img/favicon.ico" type="image/x-icon"><link rel="icon" href="web/img/favicon.ico" type="image/x-icon"></head><body><div id="header"><span id="header1"> <h1>'
    main += username
    main +='''</h1></span><span id="header2" class="back">
<form name="input" action="work.py" method="post">
<input type="hidden" name = "username" value="'''
    main += username
    main += '''"><input type="submit" name ="back" value="Return to your profile"></form></span>
</div>
<div id="chat">'''
    
    main += '<h1 align="center">'
    main += other
    main += '</h1>'

    #display blocked messaged
    if other in ownblock:
        main += '<p id="block">'
        main += 'You have blocked this user. They will neither be able to message you or see the messages you send them until you unblock them. Messages you send them while they are blocked, will appear to them after you unblock them.'
        main += '</p>'

    main += '<form name="input" action="work.py" method="post" align="center"><input type="hidden" name = "username" value="'
    main += username
    main +='''" />
<input type="hidden" name = "users" value="'''
    main += other
    main += '''" /><br>
To check for new messages: <input type="submit" name = "refresh" value="Refresh" />
</form><hr class="hr"><br>'''
    main += convo
    main += '<hr class="hr"><br>'
    main += '''<form name="input" action="work.py" method="post">
<script language="JavaScript">
  function selectText(textField) 
  {
    textField.focus();
    textField.select();
  }
</script>
<textarea name="text" cols="75" rows="12" onClick='selectText(this); this.onclick=null;'>Enter your message for '''
    main += other
    main +=''' here</textarea>
<input type="hidden" name = "username" value="'''
    main += username
    main +='''" />
<input type="hidden" name = "users" value="'''
    main += other
    main += '''" /><br>
<input type="submit" name = "enter" value="Send" />
</form>
</div>
<div id="bottom">
<p>&copy; 2013 Isaac Gluck and Hubert Puszklewicz</p>
<p> Mr. Jaishankar Period 9</p>
</div>'''
    return main

def chat():#Hubert - extract a conversation with someone from one's .txt file - display the conversation
    user = form['username'].value
    other = form['users'].value

    if 'text' in form:
        for i in form['text'].value:
            if i in '@$:':
                return ' <font color="red"><h1>Error. The characters "@", "$", and ":" are not allowed. We apologize for the inconvenience. <form name="input" action="work.py" method="post"><input type="hidden" name="username" value ="' + user + '"><input type="hidden" name="users" value ="' + other + '"><input type="submit" name="chat" value="Go Back"></form></h1></font>'

    if 'text' in form:
        at = strftime(" %a, %b %d, %Y - %I:%M %p ", localtime())#Isaac - using the python time module to print the time a message was sent
        message = '<p><b>' + user + ': </b>' + form['text'].value + '</p><p class="time"> Sent '
        message += at
        message += '</p><br>'
    else:
        #message input required
        return ' <font color="red"><h1>Error. Please enter a message to send. <form name="input" action="work.py" method="post"><input type="hidden" name="username" value ="' + user + '"><input type="hidden" name="users" value ="' + other + '"><input type="submit" name="chat" value="Go Back"></form></h1></font>'

    if form['text'].value == 'Enter your message for ' + other +' here':
        #message input required
        return ' <font color="red"><h1>Error. Please enter a message to send. <form name="input" action="work.py" method="post"><input type="hidden" name="username" value ="' + user + '"><input type="hidden" name="users" value ="' + other + '"><input type="submit" name="chat" value="Go Back"></form></h1></font>'

    usertxt = user + '.txt'
    othertxt = other + '.txt'

    openuser = open( 'users/' + usertxt, 'r')
    rou = openuser.read().split('$')
    openuser.close()
    
    openother = open( 'users/' + othertxt, 'r')
    roo = openother.read().split('$')
    openother.close()

    #if conversation with chosen person doesn't exist yet - create it
    if other not in rou:
        writeuser = open( 'users/' + usertxt, 'a')
        writeuser.write('$' + other)
        writeuser.write('$')
        writeuser.write(message)
        writeuser.close()

        writeother = open('users/' + othertxt, 'a')
        writeother.write('$' + user)
        writeother.write('$')
        writeother.write(message)
        writeother.close()
        
    #otherwise add to the convo (the other person's username index + 1)
    else:
        userindex = rou.index(other) + 1
        rou[userindex] = rou[userindex] + message
        userfinal = '$'.join(rou)
        finalu = open( 'users/' + usertxt, 'w')
        finalu.write(userfinal)
        finalu.close()
        
        otherindex = roo.index(user) + 1
        roo[otherindex] = roo[otherindex] + message
        otherfinal = '$'.join(roo)
        finalo = open( 'users/' + othertxt, 'w')
        finalo.write(otherfinal)
        finalo.close()

    return conversation(user, other)

def back(): #Hubert - return to profile page
    username = form['username'].value
    b = r.read().split('\n')
    r.close()

    a = '''<!DOCTYPE html>
<html>
<head>
<title>'''
    
    a += username
    
    a +='''</title>
<link type="text/css" rel="stylesheet" href="web/styles/profile.css"/>
<link rel="shortcut icon" href="web/img/favicon.ico" type="image/x-icon">
<link rel="icon" href="web/img/favicon.ico" type="image/x-icon">
</head>
<body>
<div id="header">
<span id="header1"> <h1>'''
    
    a += username
    
    a+= '''</h1> </span>
<span id="header2"> <h2><a href="web/login.html">Log Out</a></h2> </span>
</div>
<div id="chat">
<h3>Select a User to Chat With</h3>
<form name="input" action="work.py" method="post">
<select name="users">'''
    
    for i in b[:-1]:
        k = i.split(':')
        if k[0] != username:
            a += '<option>' + k[0] + '</option>'
        
    a += '''</select><br>
<input type="hidden" name="username" value='''
    a += username

    a +='''><input type="submit" name="chat" value="submit">
</form>

<h3>Blocked Users:</h3>'''
    
    m = open( 'users/' + username + '.txt', 'r')
    p = m.read().split('@')[1]
    m.close()

#    if ',' in p:
    plist = p.split(',')
    for i in plist:
        if i != '' and i != ' ':
            a += '<p>' + i + '</p>'
#    else:
#        a += '<p>' + p + '</p>'


    a +='''</div>
<div id="already">
<h3>You are chatting with:</h3>'''
    
    z = open('users/' + username + '.txt', 'r')
    prof = z.read().split('$')
    z.close()
    for i in prof:
        if i != username and i in users:
            chatting = i
            a += '<p>' + chatting + '</p>'
            
    a +='''</div>
<div id="notyet">
<h3>You are not chatting with:</h3>'''
    
    for i in users:
        if i != username and i not in prof:
            notchat = i
            a += '<p>' + notchat + '</p>'

    a += '''</div><div id="block">
    <h3>Block Users:</h3>
    Add users to your block list:
    <form name="input" action="work.py" method="post">'''
    #<script language="JavaScript">
    #function selectText(textField) 
    #{
    #textField.focus();
    #textField.select();
    #}
    #</script>
    a += '<input type="text" name="who"' #value="Usernames separated by commas" onClick='selectText(this); this.onclick=null;'
    a += ''' placeholder="Usernames seperated by commas" class="long">
    <input type = "hidden" name = "username" value= '''

    a += username

    a +=''' ><br>
    <input type ="submit" name = "block" value ="Block"><br>
    </form>'''

    a += '''<h3>Unblock Users:</h3>
    Remove users to your block list:
    <form name="input" action="work.py" method="post">
    <select name="unblock">'''

    q = open('users/' + username + '.txt', 'r')
    unblock = q.read().split('@')[1].split(',')
    q.close()
    for i in unblock:
        if i != '' and i != ' ':
            a += '<option>' + i + '</option>'


    a+= '''</select>
    <input type = "hidden" name = "username" value="'''

    a += username

    a += '''"><br>
    <input type ="submit" name = "deblock" value ="unblock"><br>
    </form></div>'''

    a +='''
<div id="bottom">
<p>&copy; 2013 Isaac Gluck and Hubert Puszklewicz</p>
<p> Mr. Jaishankar Period 9</p>
</div>
'''
    return a

 #Isaac - allow users to block people   
def block():
    username = form['username'].value
    #input required
    if 'who' not in form:
        return ' <font color="red"><h1>Error. Make sure you enter at least one username. <form name="input" action="work.py" method="post"><input type="hidden" name="username" value ="' + username + '"><input type="submit" name="back" value="Go Back"></form></h1></font>'
    
    block = form['who'].value + ','

    #usernames separated by commas
    if ' ' in block:
        return ' <font color="red"><h1>Error. Do not type spaces, just usernames separated by commas. <form name="input" action="work.py" method="post"><input type="hidden" name="username" value ="' + username + '"><input type="submit" name="back" value="Go Back"></form></h1></font>'

    blocklist = block.split(',')

    #only existing usernames can be blocked
    for i in blocklist:
        if i not in users and i != ' ' and i != '':
            return ' <font color="red"><h1>Error. Make sure you enter only valid usernames. <form name="input" action="work.py" method="post"><input type="hidden" name="username" value ="' + username + '"><input type="submit" name="back" value="Go Back"></form></h1></font>'


    ob = open( 'users/' + username + '.txt', 'r')
    re = ob.read().split('@')
    check = re[1].split(',')
    ob.close()
    for i in blocklist:
        if i in check and i != '' and i != ' ':
            #check for duplicate blocks
            return ' <font color="red"><h1>Error. You have entered the username of a user you have already blocked. <form name="input" action="work.py" method="post"><input type="hidden" name="username" value ="' + username + '"><input type="submit" name="back" value="Go Back"></form></h1></font>'


    f = open( 'users/' + username + '.txt', 'r')
    k = f.read().split('@')
    f.close()
    k[1] += ','.join(blocklist) + ','
    blocked = '@'.join(k)

    n = open( 'users/' + username + '.txt', 'w')
    n.write(blocked)
    n.close()

    b = r.read().split('\n')
    r.close()

    a = '''<!DOCTYPE html>
<html>
<head>
<title>'''
    
    a += username
    
    a +='''</title>
<link type="text/css" rel="stylesheet" href="web/styles/profile.css"/>
<link rel="shortcut icon" href="web/img/favicon.ico" type="image/x-icon">
<link rel="icon" href="web/img/favicon.ico" type="image/x-icon">
</head>
<body>
<div id="header">
<span id="header1"> <h1>'''
    
    a += username
    
    a+= '''</h1> </span>
<span id="header2"> <h2><a href="web/login.html">Log Out</a></h2> </span>
</div>
<div id="chat">
<h3>Select a User to Chat With</h3>
<form name="input" action="work.py" method="post">
<select name="users">'''
    
    for i in b[:-1]:
        k = i.split(':')
        if k[0] != username:
            a += '<option>' + k[0] + '</option>'
        
    a += '''</select><br>
<input type="hidden" name="username" value='''
    a += username
    a +='''><input type="submit" name="chat" value="submit">
</form>

<h3>Blocked Users:</h3>'''
    
    m = open( 'users/' + username + '.txt', 'r')
    p = m.read().split('@')[1]
    m.close()

    plist = p.split(',')
    for i in plist:
        if i != '' and i != ' ':
            a += '<p>' + i + '</p>'

    a +='''</div>
<div id="already">
<h3>You are chatting with:</h3>'''
    
    z = open('users/' + username + '.txt', 'r')
    prof = z.read().split('$')
    z.close()
    for i in prof:
        if i != username and i in users:
            chatting = i
            a += '<p>' + chatting + '</p>'
            
    a +='''</div>
<div id="notyet">
<h3>You are not chatting with:</h3>'''
    
    for i in users:
        if i != username and i not in prof:
            notchat = i
            a += '<p>' + notchat + '</p>'

    a += '''</div><div id="block">
    <h3>Block Users:</h3>
    <h4 class="red">You have succesfully blocked another user.</h4>
    Add users to your block list:
    <form name="input" action="work.py" method="post">'''
    #<script language="JavaScript">
    #function selectText(textField) 
    #{
    #textField.focus();
    #textField.select();
    #}
    #</script>
    a += '<input type="text" name="who"' #value="Usernames separated by commas" onClick='selectText(this); this.onclick=null;'
    a += ''' placeholder="Usernames seperated by commas" class="long">
    <input type = "hidden" name = "username" value= '''

    a += username

    a +=''' ><br>
    <input type ="submit" name = "block" value ="Block"><br>
    </form>'''

    a += '''<h3>Unblock Users:</h3>
    Remove users to your block list:
    <form name="input" action="work.py" method="post">
    <select name="unblock">'''

    q = open('users/' + username + '.txt', 'r')
    unblock = q.read().split('@')[1].split(',')
    q.close()
    for i in unblock:
        if i != '' and i != ' ':
            a += '<option>' + i + '</option>'


    a+= '''</select>
    <input type = "hidden" name = "username" value="'''

    a += username

    a += '''"><br>
    <input type ="submit" name = "deblock" value ="unblock"><br>
    </form></div>'''

    a +='''
<div id="bottom">
<p>&copy; 2013 Isaac Gluck and Hubert Puszklewicz</p>
<p> Mr. Jaishankar Period 9</p>
</div>
'''
    return a

#Isaac - remove users from the "blocked" part of a users .txt file
def unblock():
    username = form['username'].value
    if 'unblock' not in form:
        return ' <font color="red"><h1>Error. Please select someone to unblock. If you have not blocked any users, you cannot unblock any users. <form name="input" action="work.py" method="post"><input type="hidden" name="username" value ="' + username + '"><input type="submit" name="back" value="Go Back"></form></h1></font>'
    who = form['unblock'].value
    q = open('users/' + username + '.txt', 'r')
    
    first = q.read()
    unblock = first.split('@')[1].split(',')
    q.close()

    index = unblock.index(who)

    new = unblock[:index] + unblock[index + 1:]
    rejoin = first.split('@')
    rejoin[1] = ','.join(new)
    final = '@'.join(rejoin)

    w = open('users/' + username + '.txt', 'w')
    w.write(final)
    w.close()

    b = r.read().split('\n')
    r.close()

    a = '''<!DOCTYPE html>
<html>
<head>
<title>'''
    
    a += username
    
    a +='''</title>
<link type="text/css" rel="stylesheet" href="web/styles/profile.css"/>
<link rel="shortcut icon" href="web/favicon.ico" type="image/x-icon">
<link rel="icon" href="web/favicon.ico" type="image/x-icon">
</head>
<body>
<div id="header">
<span id="header1"> <h1>'''
    
    a += username
    
    a+= '''</h1> </span>
<span id="header2"> <h2><a href="web/login.html">Log Out</a></h2> </span>
</div>
<div id="chat">
<h3>Select a User to Chat With</h3>
<form name="input" action="work.py" method="post">
<select name="users">'''
    
    for i in b[:-1]:
        k = i.split(':')
        if k[0] != username:
            a += '<option>' + k[0] + '</option>'
        
    a += '''</select><br>
<input type="hidden" name="username" value='''
    a += username
    a +='''><input type="submit" name="chat" value="submit">
</form>

<h3>Blocked Users:</h3>'''
    
    m = open( 'users/' + username + '.txt', 'r')
    p = m.read().split('@')[1]
    m.close()

    plist = p.split(',')
    for i in plist:
        if i != '' and i != ' ':
            a += '<p>' + i + '</p>'

    a +='''</div>
<div id="already">
<h3>You are chatting with:</h3>'''
    
    z = open('users/' + username + '.txt', 'r')
    prof = z.read().split('$')
    z.close()
    for i in prof:
        if i != username and i in users:
            chatting = i
            a += '<p>' + chatting + '</p>'
            
    a +='''</div>
<div id="notyet">
<h3>You are not chatting with:</h3>'''
    
    for i in users:
        if i != username and i not in prof:
            notchat = i
            a += '<p>' + notchat + '</p>'

    a += '''</div><div id="block">
    <h3>Block Users:</h3>
    Add users to your block list:
    <form name="input" action="work.py" method="post">'''
    #<script language="JavaScript">
    #function selectText(textField) 
    #{
    #textField.focus();
    #textField.select();
    #}
    #</script>
    a += '<input type="text" name="who"' #value="Usernames separated by commas" onClick='selectText(this); this.onclick=null;'
    a += ''' placeholder="Usernames seperated by commas" class="long">
    <input type = "hidden" name = "username" value= '''

    a += username

    a +=''' ><br>
    <input type ="submit" name = "block" value ="Block"><br>
    </form>'''

    a += '''<h3>Unblock Users:</h3>
    <h4 class="red">You have succesfully unblocked another user.</h4>
    Remove users to your block list:
    <form name="input" action="work.py" method="post">
    <select name="unblock">'''

    q = open('users/' + username + '.txt', 'r')
    unblock = q.read().split('@')[1].split(',')
    q.close()
    for i in unblock:
        if i != '' and i != ' ':
            a += '<option>' + i + '</option>'


    a+= '''</select>
    <input type = "hidden" name = "username" value="'''

    a += username

    a += '''"><br>
    <input type ="submit" name = "deblock" value ="unblock"><br>
    </form></div>'''

    a +='''
<div id="bottom">
<p>&copy; 2013 Isaac Gluck and Hubert Puszklewicz</p>
<p> Mr. Jaishankar Period 9</p>
</div>
'''
    return a

        

#display the page that was called by the user through the many forms
if 'register' in form:
    page = '<!DOCTYPE HTML><html><head><title>Form Lab</title><link type="text/css" rel="stylesheet" href="web/styles/style.css"/><link rel="shortcut icon" href="web/img/favicon.ico" type="image/x-icon"><link rel="icon" href="web/img/favicon.ico" type="image/x-icon"></head><body>'
    page += register()

if 'login' in form:
    page += login()

if 'chat' in form:
    page += conversation('Error', 'Error')

if 'enter' in form:
    page += chat()

if 'back' in form:
    page += back()

if 'block' in form:
    page += block()

if 'deblock' in form:
    page += unblock()

if 'refresh' in form:
    page += conversation('Error', 'Error')
    
page += '</body></html>'

print page
