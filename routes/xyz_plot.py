import os
from aiohttp import web
import datetime

import folder_paths

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
        "score_log.csv",
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
