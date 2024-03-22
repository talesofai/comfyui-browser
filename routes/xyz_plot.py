import os
from aiohttp import web
import datetime
import csv
import json

import folder_paths

LOG_FILE_NAME = 'score_log.csv'

async def api_update_score(request):
    body = await request.json()
    user_uuid = body.get("user", "anonymous")
    source = body.get("source")
    score = body.get("score")

    source_arr = source.split(":")
    if len(source_arr) != 5:
        return web.Response(status=404)

    log_path = os.path.join(
        folder_paths.get_output_directory(),
        source_arr[0],
        LOG_FILE_NAME,
    )

    dtstr = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S%Z")

    # created_at, user_uuid, score, ix, iy, iz, index
    new_line = ",".join([dtstr, user_uuid, str(score), source_arr[1], source_arr[2], source_arr[3], source_arr[4]]) + '\n'
    if not os.path.exists(log_path):
        with open(log_path, "w", encoding="utf-8") as f:
            f.write(new_line)
    else:
        lines = []
        with open(log_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        pattern = ",".join([source_arr[1], source_arr[2], source_arr[3], source_arr[4]])
        lines = [line for line in lines if pattern not in line]
        lines.append(new_line)
        with open(log_path, "w", encoding="utf-8") as f:
            f.writelines(lines)

    return web.Response(status=200)

async def api_get_score_statistic(request):
    target_path = request.query.get('path')
    if not target_path:
        return web.Response(status=404)

    #/browser/s/outputs/xyz_plot_4/result.json
    if len(target_path.split('/')) < 5:
        return web.Response(status=400)

    target_path = target_path.split('/')[4]
    log_path = os.path.join(
        folder_paths.get_output_directory(),
        target_path,
        LOG_FILE_NAME,
    )
    if not os.path.exists(log_path):
        return web.Response(status=404)

    data = []
    with open(log_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            data.append(row)

    statistic = {}
    for row in data:
        if not row[3] in statistic:
            statistic[row[3]] = { 'total': 0 }
        if not row[4] in statistic[row[3]]:
            statistic[row[3]][row[4]] = { 'total': 0 }
        if not row[5] in statistic[row[3]][row[4]]:
            statistic[row[3]][row[4]][row[5]] = 0

        statistic[row[3]][row[4]][row[5]] += int(row[2])
        statistic[row[3]][row[4]]['total'] += int(row[2])
        statistic[row[3]]['total'] += int(row[2])

    result_path = os.path.join(
        folder_paths.get_output_directory(),
        target_path,
        'result.json',
    )
    xyz_result = []
    with open(result_path, 'r', encoding='utf-8') as f:
        xyz_result = json.load(f)['result']

    stat_ret = []
    for ix, _ in enumerate(xyz_result):
        vy = xyz_result[ix]['children']
        rx = {
            'type': 'axis',
            'score': statistic.get(str(ix), {}).get('total', 0),
            'children': [],
        }
        for iy, _ in enumerate(vy):
            vz = vy[iy]['children']
            ry = {
                'type': 'axis',
                'score': statistic.get(str(ix), {}).get(str(iy), {}).get('total', 0),
                'children': [],
            }
            if vz[0]['type'] == 'img':
                ry['children'].append({
                    'type': 'axis',
                    'score': statistic.get(str(ix), {}).get(str(iy), {}).get('-1', 0),
                })
            else:
                for iz, _ in enumerate(vz):
                    ry['children'].append({
                        'type': 'axis',
                        'score': statistic.get(str(ix), {}).get(str(iy), {}).get(str(iz), 0),
                    })
            rx['children'].append(ry)
        stat_ret.append(rx)


    return web.json_response({
        'result': stat_ret,
    })
