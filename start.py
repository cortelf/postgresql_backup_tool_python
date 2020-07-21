import argparse
import subprocess
import telebot
import datetime
import os
import time

parser = argparse.ArgumentParser()
parser.add_argument('-path', type=str, required=True, help="pg_dump call path")
parser.add_argument('-dbhost', type=str, required=True, help="Database host")
parser.add_argument('-dbport', type=int, required=True, help="Database port")
parser.add_argument('-dblogin', type=str, required=True, help="Database login")
parser.add_argument('-dbpassword', type=str, required=True, help="Database host")
parser.add_argument('-db', type=str, required=True, help="Database name")
parser.add_argument('-token', type=str, required=True, help="Telegram bot token")
parser.add_argument('-sid', type=str, required=True, help="Channel or user ID")
parser.add_argument('-btime', type=int, help="Sleep script time in minutes")

args = parser.parse_args()

sleep_minutes = 24 * 60
path = ""
bot = telebot.TeleBot(args.token, parse_mode=None)

while True:
    try:
        # Check bot exist
        try:
            bot.get_me()
        except Exception as ex:
            print(ex)

            raise Exception("Wrong telegram bot token")

        # Check bot chat permissions
        try:
            bot.get_chat(args.sid)
        except Exception as ex:
            print(ex)

            raise Exception("Wrong telegram sid")

        if args.btime:
            sleep_minutes = args.btime

        # Validate postgre pg_dump
        if "pg_dump" in args.path:
            path = args.path
            try:
                subprocess.Popen([path, "--help"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            except Exception as ex:
                print(ex)

                raise Exception("Wrong pg_dump")
        else:
            raise Exception("Not found pg_dump file")

        now_time = datetime.datetime.utcnow()
        file_name = f"backup-{args.db}-{now_time.day}.{now_time.month}.{now_time.year}.sql"

        # call backup
        subprocess.call(
            args=[path, "-f", file_name,
                  f"postgresql://{args.dblogin}:{args.dbpassword}@{args.dbhost}:{args.dbport}/{args.db}"],
            cwd=os.getcwd()
        )

        # send to Telegram
        with open(file_name, encoding="utf-8") as file:
            try:
                bot.send_document(args.sid, file)
            except Exception as ex:
                print(ex)

                raise Exception("Error send file")

        # remove file
        os.remove(file_name)
    except Exception as e:
        print(e)

        try:
            bot.send_message(args.sid, e)
        except:
            pass

    time.sleep(sleep_minutes * 60)
