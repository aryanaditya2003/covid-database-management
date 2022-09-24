import mysql.connector as sql
import pandas as pd
import matplotlib.pyplot as plt

mydb = sql.connect(host="localhost",
                       user='root',password='root',database='project')






print('Welcome! Here you will find stats for BRICS countries affected by covid 19:')


option=''
while option != 'exit':

     option=input('''\n1.) View country's covid stats
2.) View Covid Cases Graph
3.) View GDP Stats
4.) View GDP Graph
5.) Update Data
exit - To quit the program\n
\nEnter the choice : ''')








     if option =='1':
          cntry=input('Enter the BRICS country for which you want to view the covid stats ')
          cntrylist=[cntry]
          while cntry!='1':
               cntry=input('Enter the BRICS country for which you want to view the stats(Enter 1 to stop entering) ')
               cntrylist.append(cntry)
          cntrylist.remove('1')
          string="','".join(cntrylist)

          #Querying Data from Database
          mycursor= mydb.cursor()
          mycursor.execute ("SELECT Countries,Cases,Deaths,Recoveries FROM covidcases where Countries IN ('"+string+"')")
          myresult = mycursor.fetchall()

          #Outputting Data as DataFrame
          Data=pd.DataFrame(myresult,columns=['Country','Total Cases','Deaths','Recoveries'])
          print('\t\t Stats')
          print(Data)





     elif option =='2':
          cntry=input('Enter the country for which you want to plot the graph for : ')
          cntrylist=[cntry]
          while cntry!='1':
                    cntry=input('Enter the BRICS country for which you want to plot the graph for(Enter 1 to stop entering) : ')
                    cntrylist.append(cntry)
          string="','".join(cntrylist)



          mycursor=mydb.cursor()
          mycursor.execute("SELECT Countries FROM covidcases WHERE Countries IN ('"+string +"')")
          Cntry=mycursor.fetchall()


          mycursor=mydb.cursor()
          mycursor.execute("SELECT Cases FROM covidcases WHERE Countries IN ('"+string +"')")
          Cases=mycursor.fetchall()
          cases=[]
          for a in Cases:
               for b in a:
                    cases.append(b)

    

          mycursor=mydb.cursor()
          mycursor.execute("SELECT Deaths FROM covidcases WHERE Countries IN ('"+string +"')")
          Deaths=mycursor.fetchall()
          deaths=[]
          for a in Deaths:
               for b in a:
                    deaths.append(b)


          CntryList=[]
          for x in Cntry:
               for t in x:
                    CntryList.append(t)


          plt.bar(CntryList,cases,color='blue',width=0.15,edgecolor='black')
          plt.xlabel('Countries')
          plt.ylabel('Cases')
          plt.title('Cases Per Country')
          plt.grid(True)
          plt.show()

          plt.bar(CntryList,deaths,color='red',width=0.15,edgecolor='black',label='Deaths')
          plt.xlabel('Countries')
          plt.ylabel('Deaths')
          plt.title('Deaths Per Country')
          plt.grid(True)
          plt.show()
          

     elif option =='3':
          cntry=input('Enter the BRICS country for which you want to view the gdp stats ')
          cntrylist=[cntry]
          while cntry!='1':
               cntry=input('Enter the BRICS country for which you want to view the gdp stats(Enter 1 to stop entering) ')
               cntrylist.append(cntry)
          cntrylist.remove('1')
          string="','".join(cntrylist)

          #Querying Data from Database
          mycursor= mydb.cursor()
          mycursor.execute ("SELECT Countries,BeforeCovid,AfterCovid from gdp where Countries IN ('"+string+"')")
          myresult = mycursor.fetchall()

          #Outputting Data as DataFrame
          Data=pd.DataFrame(myresult,columns=['Country','BeforeCovid','AfterCovid'])
          print('\t\t Stats')
          print(Data)







     elif option =='4':
          #Taking input as a list and converting to string
          cntry=input('Enter the BRICS country for which you want to plot the graph ')
          cntrylist=[cntry]
          while cntry!='1':
               cntry=input('Enter the country for which you want to plot the graph for(Enter 1 to stop entering) ')
               cntrylist.append(cntry)
          string="','".join(cntrylist)


          #Extracting Data from Database
          mycursor=mydb.cursor()
          mycursor.execute("SELECT Countries FROM gdp WHERE Countries IN ('"+string +"')")
          Cntry=mycursor.fetchall()


          #BeforeCovid
          mycursor=mydb.cursor()
          mycursor.execute("SELECT BeforeCovid FROM gdp WHERE Countries IN ('"+string +"')")
          GDPBefore=mycursor.fetchall()


          #After Covid
          mycursor=mydb.cursor()
          mycursor.execute("SELECT AfterCovid FROM gdp WHERE Countries IN ('"+string +"')")
          GDPAfter=mycursor.fetchall()

          #Re-entering Country Input to get correct data acc to country
          CntryList=[]
          for x in Cntry:
               for t in x:
                    CntryList.append(t)
          

          #Plotting Graphs
          plt.plot(CntryList,GDPBefore,c='blue',linestyle='--',marker='X')
          plt.plot(CntryList,GDPAfter,c='red',linestyle='--',marker='X')
          plt.xlabel('Country')
          plt.ylabel('GDP Growth Rate')
          plt.title('Effect Of Covid on GDP')
          plt.legend(['Before Covid','After Covid'])
          plt.grid(True)

          plt.show()







     if option == '5':
          cntry=input('Enter the country you want to update the data for : ')
          new_cases=input('Enter total updated cases : ')
          new_deaths=input('Enter total updated deaths : ')
          new_recoveries=input('Enter total updated recoveries : ')


          mycursor= mydb.cursor()
          mycursor.execute("UPDATE covidcases SET Cases ="+new_cases+",Deaths="+new_deaths+",Recoveries="+new_recoveries+" WHERE Countries = '"+cntry+"'")
          mydb.commit()

          print('Data Updated Succesfully\n')

          mycursor= mydb.cursor()
          mycursor.execute ("SELECT Countries,Cases,Deaths,Recoveries FROM covidcases")
          myresult = mycursor.fetchall()
          Data=pd.DataFrame(myresult)
          print(Data)


exit()

