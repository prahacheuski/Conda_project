from dataclasses import dataclass, field
from collections import deque
from typing import Deque
from time import sleep
import datetime
import sys


@dataclass(repr=False, frozen=True)
class Job:
    id: int = field()
    t: int = field()

    def do_the_work(self):
        sleep(self.t)

    def __repr__(self):
        return 'Job #{:0>3} ({} secs)'.format(self.id, self.t)


class JobProcessor(object):
    __slots__ = '__jobs', '__work_time_secs', '__cnt'

    def __init__(self):
        self.__jobs: Deque[Job] = deque()
        self.__work_time_secs: float = 0.
        self.__cnt: int = 0

    def add_job(self, job: Job):
        self.__jobs.append(job)

    def __process_job(self):
        st_t = datetime.datetime.now()

        job = self.__jobs.popleft()
        job.do_the_work()

        self.__cnt += 1
        self.__work_time_secs += (datetime.datetime.now() - st_t).seconds

        return job

    def perform(self):
        total = len(self.__jobs)
        cnt = 1

        def list_of_jobs():
            return '\n'.join([str(j) for j in self.__jobs])

        print(f'List of jobs:\n{list_of_jobs()}\n{"-" * (55 + total)}')

        while self.__jobs:
            job = self.__process_job()
            self.__print_progress_bar(cnt, total, prefix=f'{job} has been processed', bar_length=total)
            cnt += 1

        print(f'{self.__cnt} jobs have been processed in {self.__work_time_secs} secs')

    @staticmethod
    def __print_progress_bar(iteration, total, prefix='', suffix='Complete', decimals=1, bar_length=100):
        """
        Call in a loop to create terminal progress bar
        @params:
            iteration   - Required  : current iteration (Int)
            total       - Required  : total iterations (Int)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            bar_length  - Optional  : character length of bar (Int)
        """
        str_format = "{0:." + str(decimals) + "f}"
        percents = str_format.format(100 * (iteration / float(total)))
        filled_length = int(round(bar_length * iteration / float(total)))
        bar = '█' * filled_length + '-' * (bar_length - filled_length)

        sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix))

        if iteration == total:
            sys.stdout.write('\n')
        sys.stdout.flush()


if __name__ == '__main__':
    jobs = enumerate(sys.argv[1:], start=1)

    jp = JobProcessor()

    for job_id, job_time in jobs:
        if job_time.isdigit():
            jp.add_job(Job(id=job_id, t=int(job_time)))

    jp.perform()
