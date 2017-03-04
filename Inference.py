#	Copyright Lei Jin
#	12/2016 
from copy import deepcopy
import time
fileOpen =open("input.txt", "rb")
fileWrite=open("output.txt","w")
#dispose lines
lines=[]
aLine=fileOpen.readline()
aLine=aLine.strip('\n')#drop \n
lines.append(aLine)
while aLine:
	aLine=fileOpen.readline()
	aLine=aLine.strip('\n')#drop \n
	lines.append(aLine)
	if not aLine:
		break
# print lines
no_Test=int(lines[0])
no_KB=int(lines[int(lines[0])+1])
originalTest=lines[1:no_Test+1]
originalKB=lines[no_Test+2: no_KB+2+no_Test]
# print originalTest
# def 
# print originalKB
def clean_space(clause):
	clause=clause.replace(" ","")
	return clause

def clean_imply(clause):
	inply_index=clause.find("=>")
	c_clause=list(clause)
	# before "=>"
	stack_b=[]
	stack_b.append(')')
	# print inply_index
	for x in range(0,inply_index-1):
		if len(stack_b)==0:
			if clause[inply_index-2-x]=='(':
				break
		if clause[inply_index-2-x]==')':
			stack_b.append(')')
		if clause[inply_index-2-x]=='(':
			stack_b.pop()
	c_clause.insert(inply_index-1-x,"(~")

	inply_index+=1
	# after the "=>"
	stack_f=[]
	c_clause[inply_index]=')'
	c_clause[inply_index+1]='|'
	index_forward=inply_index+2
	# get the next "("
	for x in range(index_forward,len(c_clause)):
		if c_clause[x]=="(":
			break		
	index_next=x
	stack_f.append("(")
	for x in range(index_next+1,len(c_clause)):
		if len(stack_f)==0:
			if c_clause[index_next]==')':
				break
		if c_clause[index_next]=="(":
			stack_f.append("(")
		if c_clause[index_next]==")":
			stack_f.pop()
	clause=""
	for x in range(len(c_clause)):
		clause+=c_clause[x]
	return clause

def distribute_negation(clause):
	c_clause=list(clause)
	index1=0
	length=len(c_clause)
	while index1<length:
		print clause
		print c_clause
		print index1
		print c_clause[index1+1:].count("~")
		if c_clause[index1+1:].count("~")!=0:
			neg_index=c_clause[index1+1:].index("~")+index1+1
			index1=neg_index			
		else:
			clause=""
			for x in range(len(c_clause)):
				clause+=c_clause[x]
			return clause

		if c_clause[neg_index+1]!="(":
			continue
		else:
			c_clause[neg_index+1]
			stack=2
			index_next=c_clause[neg_index+2:].index("(")+neg_index+2
			mem1=0
			mem2=0
			unique=0
			for x in range(index_next+1,length):
				if stack==1 and unique==0:
					mem1=x-1
					unique=1
				if stack==0:
					mem2=x
				if c_clause[x]=="(":
					stack+=1
				if c_clause[x]==")":
					stack-=1
			if  c_clause[mem1+1]==")":
				if c_clause[neg_index+2]=="~":
					del c_clause[mem1+2]
					del c_clause[mem1+1]
					del c_clause[neg_index+2]
					del c_clause[neg_index+1]
					del c_clause[neg_index]
					del c_clause[neg_index-1]
					length=len(c_clause)
					index1=0
					continue
			if clause[mem1+1]=="|":
				c_clause[mem1+1]="&"
				c_clause.insert(mem1+2,"~")
				c_clause.insert(mem1+2,"(")
				c_clause.insert(mem1+1,")")
				c_clause[neg_index]="("
				c_clause[neg_index+1]="~"
				length=len(c_clause)
				clause=""
				for x in range(len(c_clause)):
					clause+=c_clause[x]
				continue
			if clause[mem1+1]=="&":
				c_clause[mem1+1]="|"
				c_clause.insert(mem1+2,"~")
				c_clause.insert(mem1+2,"(")
				c_clause.insert(mem1+1,")")
				c_clause[neg_index]="("
				c_clause[neg_index+1]="~"
				length=len(c_clause)
				clause=""
				for x in range(len(c_clause)):
					clause+=c_clause[x]
				continue

def check_mid(clause):
	flag=0
	if clause.find("&")==-1 and clause.find("|")==-1:
		return [0,0]
	stack=1
	for x in range(1,len(clause)):
		if stack==1 and flag!=0:
			return [clause[x],x]
		if clause[x]=="(":
			stack+=1
			flag=1
		if clause[x]==")":
			stack-=1
			flag=1

def recursive(clause):
	c_clause=list(clause)
	if c_clause.count("&")==0:
		return clause
	if c_clause.count("|")==0:
		return clause
	m=check_mid(clause)
	if m[0]==0:
		return clause
	if m[0]=="|":
		l=clause[1:m[1]:]
		r=clause[m[1]+1:len(clause)-1:]
		mml=check_mid(l)
		mmr=check_mid(r)
		if mml[0]=="&":
			ll=l[1:mml[1]:]
			lr=l[mml[1]+1:len(l)-1:]
			clause="(("+ll+'|'+r+')&('+lr+'|'+r+"))"
			l=recursive(clause)
			return l
		elif mml[0]=="|":
			l=recursive(l)
		l=l.replace("*","&")

		if mmr[0]=="&":
			rl=r[1:mmr[1]:]
			rr=r[mmr[1]+1:len(r)-1:]
			clause="(("+l+'|'+rl+')&('+l+'|'+rr+"))"
			r=recursive(clause)
			r=r.replace("*","&")
			return r
		elif mmr[0]=="|":
			r=recursive(r)
			clause="("+l+'|'+r+")"
			clause=clause.replace("*","&")
			clause=recursive(clause)
			return clause
		else:
			clause="("+l+'|'+r+")"
			clause=recursive(clause)
			clause=clause.replace("*","&")
			clause=recursive(clause)
		return clause
	elif m[0]=="&":
		l=clause[1:m[1]:]
		r=clause[m[1]+1:len(clause)-1:]
		if l.find("&")==-1 and r.find("&")==-1:
			clause="("+l+"*"+r+")"
			return clause
		elif l.find("&")==-1 and r.find("&")!=-1:
			r=recursive(r)
			clause="("+l+"*"+r+")"
			return clause
		elif l.find("&")!=-1 and r.find("&")==-1:
			l=recursive(l)
			clause="("+l+"*"+r+")"
			return clause
		else:
			l=recursive(l)
			r=recursive(r)
			clause="("+l+"*"+r+")"
		clause=recursive(clause)		
	return clause

def gothrouth_and_mid(clause):
	stack=1
	flag=0
	for x in range(1,len(clause)):
		if stack==1 and flag!=0:
			return x
		if clause[x]=="(":
			stack+=1
			flag=1
		if clause[x]==")":
			stack-=1
			flag=1
		
def get_sentence(clause,result):
	if clause.find("&")==-1:
		result.append(clause)
		return result
	index=gothrouth_and_mid(clause)
	l=clause[1:index]
	r=clause[index+1:len(clause)-1]
	get_sentence(l,result)
	get_sentence(r,result)
	return result

def gothrouth_or_mid(clause):
	stack=1
	flag=0
	for x in range(1,len(clause)):
		if stack==1 and flag!=0:
			return x
		if clause[x]=="(":
			stack+=1
			flag=1
		if clause[x]==")":
			stack-=1
			flag=1
			
def get_literals(clause,result):
	if clause.find("|")==-1:
		result.append(clause)
		return result
	index=gothrouth_or_mid(clause)
	l=clause[1:index]
	r=clause[index+1:len(clause)-1]
	get_literals(l,result)
	get_literals(r,result)
	return result

def to_cnf(originalKB):
	resultKB=[]
	for x in range(len(originalKB)):
		originalKB[x]=clean_space(originalKB[x])
	for x in range(0,len(originalKB)):
		while(originalKB[x].find("=>")!=-1):
			originalKB[x]=clean_imply(originalKB[x])
		originalKB[x]=distribute_negation(originalKB[x])
		print originalKB
		originalKB[x]=recursive(originalKB[x])
		originalKB[x]=originalKB[x].replace("*","&")
		result=[]
		resultKB.append(get_sentence(originalKB[x],result))
	temp=[]
	for x in range(len(resultKB)):
		for y in range(len(resultKB[x])):
			temp.append(resultKB[x][y])
	resultKB=temp
	return resultKB

def get_inners(inner):
	if inner.find(",")==-1:
		return [inner]
	temp=inner.split(',')
	result=[]
	for x in temp:
		result.append(x)
	return result

def formalizeKB(KB):
	forKB=[]#the whole kb including forST 
	for sentence in KB:
		forST=[]#the whole sentences including predicts
		result_of_get_literals=[]
		disjunct=get_literals(sentence,result_of_get_literals)# get all the notations,like:A(x),B(x,y)...
		# print disjunct
		for predict in disjunct:
			forNT=[]#0 negative,1 name,2 variable, 3 constant
			if predict.find("~")==-1:
				negative=0
				indexname=predict.find("(")
				name=predict[0:indexname]
				forNT.append(negative)
				forNT.append(name)
				innerlist=predict[indexname+1:len(predict)-1]
			else:
				negative=1
				indexname=predict[2:len(predict)].find("(")+2
				name=predict[2:indexname]
				forNT.append(negative)
				forNT.append(name)
				innerlist=predict[indexname+1:len(predict)-2]		
			inners=get_inners(innerlist)
			forNT.append(inners)
			forST.append(forNT)
		forKB.append(forST)	
	return forKB


def formalizeTest(Test):
	forKB=[]#the whole kb including forST 
	disjunct=Test
	for predict in disjunct:
		forNT=[]#0 negative,1 name,2 variable, 3 constant
		if predict.find("~")==-1:
			negative=0
			indexname=predict.find("(")
			name=predict[0:indexname]
			forNT.append(negative)
			forNT.append(name)
			innerlist=predict[indexname+1:len(predict)-1]
		else:
			negative=1
			indexname=predict[1:len(predict)].find("(")+1
			name=predict[1:indexname]
			forNT.append(negative)
			forNT.append(name)
			innerlist=predict[indexname+1:len(predict)-1]		
		inners=get_inners(innerlist)
		forNT.append(inners)
		forKB.append(forNT)	
	return forKB

def negateTest(Test):
	for notations in Test:
		if notations[0]==1:
			notations[0]=0
		else:
			notations[0]=1
	return Test

def match_pattern_first(ss1,ss2):
	cp1=[]
	cp2=[]
	for x in range(len(ss1)):
		if ord(ss1[x][0])>=65 and ord(ss1[x][0])<=90:
			cp1.append([ss1[x],x])
	for x in range(len(ss2)):
		if ord(ss2[x][0])>=65 and ord(ss2[x][0])<=90:
			cp2.append([ss2[x],x])
	for x1 in cp1:
		for x2 in cp2:
			if x1[1]==x2[1] and x1[0]!=x2[0]:
				return False
	return True

def is_variable(a):
	if ord(a[0])>=97 and ord(a[0])<=122:
		return True
	else:
		return False

def build_dic(sentence):
	dic=[]
	for notations in sentence:
		for x in notations[2]:
			if is_variable(x):
				dic.append(x)
	return dic

def standerize(ss1,ss2): #s1:KBsentence s2:query
	s1=ss1[:]
	s2=deepcopy(ss2)
	dic=build_dic(s1)
	for notations in s2:
		for x in range(len(notations[2])):
			if is_variable(notations[2][x]):
				while dic.count(notations[2][x])!=0:
					notations[2][x]='n'+notations[2][x]
	return s2

def match_notion(ss1,ss2):#ss1:kbsentence,ss2:testsentence
	for x in range(len(ss1)):
		for y in range(len(ss2)):
			if ss1[x][0]!=ss2[y][0] and ss1[x][1]==ss2[y][1] and match_pattern_first(ss1[x][2],ss2[y][2]):
				return [x,y]
	return [-1,-1]

def unify_variables(ss1,ss2):#s1:KBsentence s2:query
	s1=deepcopy(ss1)
	s2=deepcopy(ss2)
	indexs=match_notion(s1,s2)
	index1=indexs[0]
	index2=indexs[1]
	theta={}
	for x in range(len(ss1[index1][2])):
		if is_variable(ss1[index1][2][x]) and is_variable(ss2[index2][2][x]):
			theta[ss2[index2][2][x]]=ss1[index1][2][x]
	thetabase=theta.keys()
	for notations_T in s2:
		for x in range(len(notations_T[2])):
			if thetabase.count(notations_T[2][x])!=0:
				notations_T[2][x]=theta[notations_T[2][x]]
	return [s2,theta]

def unify_constant(ss1,ss2):
	s1=deepcopy(ss1)
	s2=deepcopy(ss2)
	theta1={}#s1:s2
	theta2={}#s2:s1
	for notations_KB in s1:
		for notations_T in s2:
			if notations_KB[0]!=notations_T[0] and notations_KB[1]==notations_T[1] and match_pattern_first(notations_KB[2],notations_T[2]):
				for x in range(len(notations_T[2])):
					if not is_variable(notations_T[2][x]) and is_variable(notations_KB[2][x]):
						theta2[notations_KB[2][x]]=notations_T[2][x]
					elif (notations_T[2][x]) and not is_variable(notations_KB[2][x]):
						theta1[notations_T[2][x]]=notations_KB[2][x]
	if len(theta1)==0 and len(theta2)==0:#fail
		return [s1,s2,theta1,theta2]
	thetabase1=theta1.keys()
	thetabase2=theta2.keys()
	# print thetabase1
	for notations_T in s2:
		for x in range(len(notations_T[2])):
			if thetabase1.count(notations_T[2][x])!=0:
				notations_T[2][x]=theta1[notations_T[2][x]]
	for notations_KB in s1:
		for x in range(len(notations_KB[2])):
			# print notations_KB[2]
			if thetabase2.count(notations_KB[2][x])!=0:
				notations_KB[2][x]=theta2[notations_KB[2][x]]
	# print s1
	# print s2
	return [s1,s2,theta1,theta2]

def match_pattern(ss1,ss2):

	cp1=[]
	cp2=[]
	for x in range(len(ss1)):
		if ord(ss1[x][0])>=65 and ord(ss1[x][0])<=90:
			cp1.append([ss1[x],x])
	for x in range(len(ss2)):
		if ord(ss2[x][0])>=65 and ord(ss2[x][0])<=90:
			cp2.append([ss2[x],x])

	if cp1==cp2:
		# print True
		return True
	else:
		# print False
		return False

def connect(s1,s2,k,t):
	ss1=deepcopy(s1)
	ss2=deepcopy(s2)
	del ss1[k]
	del ss2[t]
	l=[]

	for n1 in ss1:
		for x in range(len(ss2)):
			if n1==ss2[x]:
				del ss2[x]
				break
			if match_pattern(n1[2],ss2[x][2]):
				del ss2[x]
				break
	for x in ss1:
		l.append(x)
	for x in ss2:
		l.append(x)

	return l

def match_in_reduce1(ss1,ss2):
	cp1=[]
	cp11=[]
	cp12=[]
	cp2=[]
	cp22=[]
	cp23=[]
	for x in range(len(ss1)):
		if ord(ss1[x][0])>=65 and ord(ss1[x][0])<=90:
			cp1.append(ss1[x])
			cp11.append(x)
			cp12.append([ss1[x],x])
	for x in range(len(ss2)):
		if ord(ss2[x][0])>=65 and ord(ss2[x][0])<=90:
			cp2.append(ss2[x])
			cp22.append(x)
			cp23.append([ss1[x],x])
	for x in cp1:
		if cp2.count(x)==0:
			return False
	for x in cp2:
		if cp1.count(x)==0:
			return False
	for x1 in cp12:
		for x2 in cp23:
			if x1[1]==x2[1] and x1[0]!=x2[0]:
				return False
	return True

def match_in_reduce2(ss1,ss2):

	m=0
	t=0
	for x in range(len(ss1)):
		if is_variable(ss1[x]):
			if not is_variable(ss2[x]):
				m=1
		if is_variable(ss2[x]):
			if not is_variable(ss1[x]):
				t=1
	if m==1 and t==0:
		# print True
		return True
	else:
		# print False
		return False

def reduce_redundant(sentence1):
	sentence=deepcopy(sentence1)
	todo=[]
	for x in range(len(sentence1)):
		for y in range(len(sentence)):
			if sentence1[x][0:2]==sentence[y][0:2] and match_in_reduce1(sentence1[x][2],sentence1[y][2]) and x!=y and todo.count(y)==0:
				todo.append(x)
				continue
			if sentence1[x][0:2]==sentence[y][0:2] and (not match_pattern_first(sentence1[x][2],sentence1[y][2])) and x!=y and todo.count(y)==0:
				continue
			if sentence1[x][0:2]==sentence[y][0:2] and match_in_reduce2(sentence1[x][2],sentence1[y][2]) and x!=y and todo.count(y)==0:
				todo.append(x)

	todo=list(set(todo))

	for x in todo[::-1]:
		del sentence[x]

	return sentence

def same_sentence_l(ss1,ss2):
	s1=deepcopy(ss1)
	s2=deepcopy(ss2)
	ls1=len(s1)
	ls2=len(s2)
	if ls1!=ls2:
		return False
	for x in range(len(s1)):
		g=0
		for y in range(len(s2)):
			if s1[x][0]==s2[y][0] and s1[x][1]==s2[y][1] and match_pattern_first(s1[x][2],s2[y][2]):
				g=1
		if g==0:
			return False
	return True


	
def unify(KB1,test_sentence1):#Test is a sentence:[ [1, 'F', ['Bob']],...]
	# print KB1
	clock=time.time()
	KB=deepcopy(KB1)
	newlist=[]
	newlist.append(test_sentence1[:])
	while len(newlist)!=0 and time.time()-clock<10:
		test_sentence1=deepcopy(newlist.pop(0))
		test_sentence=deepcopy(test_sentence1)

		can_unifyKB=[]
		for sentence_KB in KB:
			flag_unify=0
			for notations_KB in sentence_KB:
				for notations_T in test_sentence:

					if notations_KB[0]!=notations_T[0] and notations_KB[1]==notations_T[1] and match_pattern_first(notations_T[2],notations_KB[2]):
						flag_unify=1

						unify_notion_name=notations_KB[1]
						break
			if flag_unify==1 and can_unifyKB.count(sentence_KB)==0:

				sentence_KBtemp=deepcopy(sentence_KB)
				can_unifyKB.append(sentence_KBtemp)

		if len(can_unifyKB)==0:
			if KB.count(test_sentence)==0:
				KB.append(deepcopy(test_sentence))
			continue
		test_sentencetemp=deepcopy(test_sentence1)

		for sentence_KB in can_unifyKB:

			test_sentence=deepcopy(test_sentencetemp)
			test_sentence=standerize(sentence_KB,test_sentence)

			# print test_sentence
			temp1=unify_variables(sentence_KB,test_sentence)#unify variables
			test_sentence=temp1[0]
			# print test_sentence
			temp2=unify_constant(sentence_KB,test_sentence)
			const_KB_sentence=temp2[0]
			const_T_sentence=temp2[1]
			K=0
			T=0
			flag_same=0
			# print const_KB_sentence
			# print const_T_sentence
			for notations_KB in const_KB_sentence:
				K+=1
				T=0
				# print notations_KB
				for notations_T in const_T_sentence:
					T+=1
					# print notations_T
					# print notations_KB
					if notations_KB[0]!=notations_T[0] and notations_KB[1:]==notations_T[1:]:
						flag_same=1
						# print flag_same
						break
				if flag_same==1:
					break
			l=connect(const_KB_sentence,const_T_sentence,K-1,T-1)

			if len(l)==0:
				return True

			l=reduce_redundant(l)

			ffg=0
			if KB.count(l)==0 and newlist.count(l)==0:
				newlist.append(l)
		if KB.count(test_sentence1)==0:
			KB.append(test_sentence1)

	return False


result_KB=to_cnf(originalKB)
# print result_KB
FKB=formalizeKB(result_KB)
TB=negateTest(formalizeTest(originalTest))
# print FKB
# print formalizeTest(originalTest)
def ret(FKB,TB):
	back=[]
	for x in range(len(TB)):
		q=deepcopy(FKB)
		b=unify(q,[TB[x]])
		back.append(b)
	s=""
	for x in back:
		if x: 
			s=s+"TRUE"+'\n'
		else:
			s=s+"FALSE"+'\n'
	fileWrite.write(s)
	print s
ret(FKB,TB) 

