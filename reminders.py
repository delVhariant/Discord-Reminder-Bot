import sqlite3
from datetime import datetime
# Simple reminder manager that provides functions to create, list and stop reminders.
# Reminders will be stored in reminders.db
class Reminders:

    def __init__(self):
        con = sqlite3.connect('reminders.sqlite')
        # Create table if it doesn't exist
        con.execute('''CREATE TABLE IF NOT EXISTS reminders
               (id INTEGER PRIMARY KEY AUTOINCREMENT,
                user TEXT NOT NULL,
                message TEXT NOT NULL,
                paused BOOLEAN NOT NULL CHECK (paused IN (0, 1)),
                interval TEXT NOT NULL CHECK (interval in ('daily', 'weekly', 'monthly')),
                last_run DATETIME,
                start DATETIME NOT NULL,
                channel TEXT NOT NULL)''')
        con.commit()
        con.close()

    def help(self):
        return '''
          User: Should be an @mention ie: @username.
          Message: Wrap the message in quotes, ie: "Take your medicine"
          Interval: Wrap in quotes, specify start date/time, then interval ie: "24/06/2022 15:00 daily"
          Supported intervals are: daily, weekly, monthly.          
          '''

    def create_reminder(self, user, interval, message, channel):
        interval_tokens = interval.split(' ')
        if len(interval_tokens) != 3:
            response = f'Invalid  interval {interval} provided. Interval must be in format "dd/mm/yyy hh:mm"'
        else:
            start = f'{interval_tokens[0]} {interval_tokens[1]}'
            start_time = datetime.strptime(start, "%d/%m/%Y %H:%M").timestamp()
            # print(start_time)
            repeat = interval_tokens[2]
            con = self.get_connection()
            query = f"INSERT INTO reminders(user, message, paused, interval, start, channel) VALUES('{user}','{message}', 0, '{repeat}','{start_time}', '{channel}')"
            # print(query)
            con.execute(query)
            con.commit()
            con.close()
            response= f'New reminder created for {user}: {message}, starting at: {start} repeat at interval: {repeat}'
        return response

    def list_reminders(self):
        con = self.get_connection('ro')
        results = con.execute('SELECT * FROM reminders').fetchall()
        clean_results = []
        for r in results:
            clean_results.append(f"ID: {r['id']}. User: {r['user']}. Reminder: {r['message']} Paused: {r['paused']==1}." \
            f"Starts: {self.epoch_to_string(r['start'])} Repeat: {r['interval']} Last Run: {self.epoch_to_string(r['last_run'])}. ChannelID: {r['channel']}")
        return clean_results

    def update_last_run(self, reminder_id):
        con = self.get_connection()
        last_run = datetime.now().timestamp()
        con.execute(f"UPDATE reminders SET last_run = {last_run} WHERE id = {reminder_id}")
        con.commit()
        con.close()

    def pause_reminder(self, reminder_id):
        con = self.get_connection()
        con.execute(f'UPDATE reminders SET paused = 1 WHERE id = {reminder_id}')
        con.commit()
        rem = con.execute(f'SELECT * FROM reminders WHERE id = {reminder_id}').fetchone()
        con.close()
        return f"Reminder: {rem['id']} - {rem['message']} for user: {rem['user']} is paused."

    def unpause_reminder(self, reminder_id):
        con = self.get_connection()
        con.execute(f'UPDATE reminders SET paused = 0 WHERE id = {reminder_id}')
        con.commit()
        rem = con.execute(f'SELECT * FROM reminders WHERE id = {reminder_id}').fetchone()
        con.close()
        return f"Reminder: {rem['id']} - {rem['message']} for user: {rem['user']} is unpaused."

    def delete_reminder(self, reminder_id):
        con = self.get_connection()
        rem = con.execute(f'SELECT * FROM reminders WHERE id = {reminder_id}').fetchone()
        
        con.execute(f"DELETE FROM reminders WHERE id = {reminder_id}")
        con.commit()
        con.close()
        return f"Reminder: {rem['id']} - {rem['message']} for user: {rem['user']} is deleted."

    def get_active_reminders(self):
        con = self.get_connection('ro')
        results = []
        for r in con.execute(f"SELECT * FROM reminders WHERE paused = 0 AND {datetime.now().timestamp()} > start").fetchall():
            results.append({'id': r['id'], 'user': r['user'], 'message': r['message'], 'last_run': r['last_run'], 'interval': r['interval'], 'start': r['start'], 'channel': r['channel']})
        return results
        

    def get_connection(self, mode='rw'):        
        con = sqlite3.connect(f'file:reminders.sqlite?mode={mode}', uri=True)
        con.row_factory = sqlite3.Row
        return con
        
    def epoch_to_string(self, epoch):
        if epoch is not None:
            ts = datetime.fromtimestamp(epoch)
            return ts.strftime("%d/%m/%Y %H:%M")
        else:
            return None





