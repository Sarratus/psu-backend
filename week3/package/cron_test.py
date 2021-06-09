from crontab import CronTab
import os


ROOT_PATH = os.path.abspath(os.curdir)
FIB_PATH = os.path.join(ROOT_PATH, 'fibonacci.py')
COMMAND = 'python' + FIB_PATH

TIMINGS = [             # Строки cron для составления расписания
    '15 15 */1 * *',    # --- каждый день в 15:15
    '0 */3 * * *',      # --- каждые 3 часа в **:00
    '00 00 * * SUN',    # --- каждое воскресение в 00:00
]


if __name__ == '__main__':
    cron = CronTab(user="User")

    for timing in TIMINGS:
        job = cron.new(command=COMMAND)
        job.setall(timing)
        cron.write()
