import socket
import tkinter as tk

# إعداد واجهة المستخدم
root = tk.Tk()
root.title("لعبة حجر ورقة مقص - العميل")

# إنشاء متغيرات
player_score = 0
client_score = 0

# تحديد إجراء عند النقر على زر اللاعب
def player_choice_handler(choice):
    global player_score, client_score
    player_choice = choice

    # إعداد اتصال Socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 9999))

    # إرسال خيار اللاعب إلى الخادم
    client_socket.send(player_choice.encode())

    # استلام اختيار الخادم
    server_choice = client_socket.recv(1024).decode()

    # تحديد الفائز
    winner = determine_winner(player_choice, server_choice)
    if winner == "player":
        player_score += 1
    elif winner == "client":
        client_score += 1

    # إظهار نتائج اللعبة
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, "اختيارك: {}\n".format(player_choice))
    result_text.insert(tk.END, "اختيار الخادم: {}\n".format(server_choice))
    result_text.insert(tk.END, "نقاط اللاعب: {}\n".format(player_score))
    result_text.insert(tk.END, "نقاط الخادم: {}\n".format(client_score))

    # التحقق من الفائز
    if player_score == 5:
        result_text.insert(tk.END, "اللاعب فاز!")
        rock_button.config(state=tk.DISABLED)
        paper_button.config(state=tk.DISABLED)
        scissors_button.config(state=tk.DISABLED)
    elif client_score == 5:
        result_text.insert(tk.END, "الخادم فاز!")
        rock_button.config(state=tk.DISABLED)
        paper_button.config(state=tk.DISABLED)
        scissors_button.config(state=tk.DISABLED)

    client_socket.close()

# تحديد الفائز بين الاختيارات
def determine_winner(player_choice, server_choice):
    # اقترانات الفوز الممكنة
    win_conditions = {
        "rock": "scissors",
        "paper": "rock",
        "scissors": "paper"
    }

    if player_choice == server_choice:
        return "tie"
    elif win_conditions[player_choice] == server_choice:
        return "player"
    else:
        return "client"

# إنشاء أزرار اللاعب
rock_button = tk.Button(root, text="حجر", command=lambda: player_choice_handler("rock"),bg="blue")
rock_button.pack()

paper_button = tk.Button(root, text="ورقة", command=lambda: player_choice_handler("paper"),bg="white")
paper_button.pack()

scissors_button = tk.Button(root, text="مقص", command=lambda: player_choice_handler("scissors"),bg="red")
scissors_button.pack()

# إنشاء مربع النتائج
result_text = tk.Text(root)
result_text.pack()

root.mainloop()
