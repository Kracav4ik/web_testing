import os
import subprocess
from tempfile import NamedTemporaryFile

import sys
from pyramid.response import Response
from pyramid.view import view_config


class RunnersMap:
    def __init__(self):
        self.runner_ids = {}
        self.next_id = 1

    def new_id(self):
        self.next_id += 1
        return self.next_id - 1

    def get(self, key):
        return self.runner_ids.get(key, {})

    def set(self, key, value):
        self.runner_ids[key] = value

    def get_latest(self):
        return self.get(max(self.runner_ids.keys(), default=0))


runners = RunnersMap()


class TaskInfo:
    def __init__(self, is_solved, failed_tries, solve_time=None):
        self.is_solved = is_solved
        self.failed_tries = failed_tries
        self.solve_time = solve_time


class TeamInfo:
    def __init__(self, name, tasks, penalty):
        self.name = name
        self.tasks = tasks
        self.penalty = penalty

    @property
    def solved_count(self):
        i = 0
        for v in self.tasks.values():
            if v.is_solved:
                i += 1
        return i


@view_config(route_name='home', renderer='templates/home.jinja2')
def show_standings(request):
    return {
        'triesTotal': '646',
        'triesPassed': '33',
        'lastTeam': 'nms (guess who)',
        'lastTask': 'A',
        'lastTime': '1:20:03',
        'tasks': 'ABCDEFGHIJK',
        'teams': [
            TeamInfo(
                "Team Sereja (Сергей Слотин, Антонио Вивальди, Никколо Паганини)",
                {
                    "A": TaskInfo(True, 0, "16:17"),
                    "B": TaskInfo(True, 0, "126:04"),
                    "C": TaskInfo(True, 0, "241:52"),
                    "D": TaskInfo(True, 2, "41:32"),
                    "E": TaskInfo(True, 0, "149:08"),
                    "G": TaskInfo(True, 0, "176:57"),
                    "H": TaskInfo(True, 0, "3:10"),
                    "I": TaskInfo(True, 0, "110:38"),
                    "J": TaskInfo(True, 1, "102:11"),
                    "K": TaskInfo(True, 1, "75:39"),
                },
                1119
            ),
            TeamInfo(
                "Мытищи, Школа Программистов - 1 (Николенко Даниил, Ковальков Дмитрий, Гаев Александр)",
                {
                    "A": TaskInfo(True, 0, "75:23"),
                    "B": TaskInfo(True, 0, "53:15"),
                    "C": TaskInfo(True, 0, "267:25"),
                    "D": TaskInfo(True, 0, "83:54"),
                    "E": TaskInfo(True, 0, "166:11"),
                    "G": TaskInfo(True, 1, "211:55"),
                    "H": TaskInfo(True, 0, "44:03"),
                    "I": TaskInfo(True, 0, "80:53"),
                    "J": TaskInfo(True, 1, "107:11"),
                    "K": TaskInfo(True, 0, "57:44"),
                },
                1183
            ),
            TeamInfo(
                "Витебск01 (Артур Петуховский, Марк Корнейчик, Владимир Кунцевич)",
                {
                    "A": TaskInfo(True, 0, "27:18"),
                    "B": TaskInfo(True, 0, "97:13"),
                    "D": TaskInfo(True, 1, "11:19"),
                    "E": TaskInfo(True, 0, "123:23"),
                    "F": TaskInfo(False, 1),
                    "G": TaskInfo(True, 0, "166:57"),
                    "H": TaskInfo(True, 0, "5:52"),
                    "I": TaskInfo(True, 2, "148:15"),
                    "J": TaskInfo(True, 1, "58:01"),
                    "K": TaskInfo(True, 0, "73:04"),
                },
                788
            ),
            TeamInfo(
                "gym2mog (Александр Керножицкий, Дмитрий Клебанов, Евгений Тумащик)",
                {
                    "A": TaskInfo(True, 0, "31:25"),
                    "B": TaskInfo(True, 0, "151:43"),
                    "D": TaskInfo(True, 0, "38:31"),
                    "E": TaskInfo(True, 0, "186:12"),
                    "G": TaskInfo(True, 1, "248:34"),
                    "H": TaskInfo(True, 0, "15:41"),
                    "I": TaskInfo(True, 2, "121:14"),
                    "J": TaskInfo(True, 0, "56:04"),
                    "K": TaskInfo(True, 0, "95:27"),
                },
                1001
            ),
            TeamInfo(
                "Saint Veronika (Арсений Бабушкин, Константин Махнёв, Дмитрий Рыбин)",
                {
                    "A": TaskInfo(True, 0, "13:42"),
                    "B": TaskInfo(True, 0, "122:09"),
                    "D": TaskInfo(True, 0, "25:52"),
                    "E": TaskInfo(True, 2, "269:18"),
                    "G": TaskInfo(True, 1, "177:04"),
                    "H": TaskInfo(True, 0, "12:50"),
                    "I": TaskInfo(True, 3, "92:23"),
                    "J": TaskInfo(True, 3, "102:52"),
                    "K": TaskInfo(True, 0, "51:52"),
                },
                1043
            ),
            TeamInfo(
                "Lyceum BSU #1 (Даниил Мельниченко, Анищенко Денис, Михнюк Роман)",
                {
                    "A": TaskInfo(True, 2, "60:54"),
                    "B": TaskInfo(True, 2, "166:20"),
                    "D": TaskInfo(True, 1, "46:54"),
                    "E": TaskInfo(True, 0, "198:28"),
                    "F": TaskInfo(False, 1),
                    "G": TaskInfo(True, 2, "245:27"),
                    "H": TaskInfo(True, 0, "23:45"),
                    "I": TaskInfo(True, 4, "192:56"),
                    "J": TaskInfo(True, 1, "90:23"),
                    "K": TaskInfo(True, 0, "108:07"),
                },
                1368
            ),
        ],
    }


@view_config(route_name='submit', renderer='templates/submit.jinja2')
def submit_page(request):
    program_file = request.POST.get("program")
    if program_file is not None and program_file != b'':
        file_contents = program_file.file.read().decode('utf-8')
        file_name = program_file.disposition_options["filename"]
        new_id = runners.new_id()
        temp = NamedTemporaryFile(mode="w+", delete=False)
        with temp:
            temp.write(file_contents)
        data = {
            "temp_file": temp.name,
            "submit_id": new_id,
            "contents": file_contents,
            "name": file_name,
            "status": "RUNNING",
        }
        runners.set(new_id, data)
        subprocess.Popen([sys.executable, "web_testing/test_run.py", str(new_id), temp.name])
        return data
    return runners.get_latest()


@view_config(route_name='answer')
def answer_page(request):
    run_id = request.GET.get("run_id")
    if run_id:
        result = request.GET.get("result")
        run_id = int(run_id)
        data = runners.get(run_id)
        data["status"] = result
        os.remove(data["temp_file"])
    return Response('')
