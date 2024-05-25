import requests
import json
import sqlite3


#API-ს გადაეცემა ინფუთით შეყვანილი სახელი, რომელსაც ამუშავებს და ალოგირთმის საშუალებით გამოითვლის
#სავარაუდოდ ასაკს, ასევე აბრუნებს ინფორმაციას თუ მერამდენედ მისდის მოთხოვნა ამ სახელთან დაკავშირებით.
#(ბოლოს ხსენებული ინფორმაცია ლაივ რეჟიმში არ ახლდება)

name = str(input("Enter your name: "))
url = f"https://api.agify.io/?name={name}"

result = requests.get(url)
# print(result)
# print(result.text)

result2 = result.json()

print(f"status code : {result.status_code}\n"
      f"Headers : {result.headers}\n"
      f"Content Type : {result.headers['Content-Type']}\n"
      f"Because of your name, I think your age is {result2['age']}\n"
      f"Information about the name {name} has been requested {result2['count']} times already.")

#ინფორმაცია Json ფორმატით ინახება .json ფაილში

with open('info.json', 'w') as file:
    json.dump(result2, file, indent=4)

#ინფორმაცია შეყვანილი სახელისა და დაბრუნებული ასაკის შესახებ ინახება ცხრილში - main,
#რომელშიც იგი ინომრება და ყველა სახელსა და მწკრივს ენიჭება უნიკალური ნომერი

conn = sqlite3.connect('info.sqlite')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS main
(id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
age INTEGER,
count INTEGER
)''')

info = (name, result2['age'], result2['count'])
c.execute('insert into main (name, age, count) values (?, ?, ?)', info)

conn.commit()
conn.close()
