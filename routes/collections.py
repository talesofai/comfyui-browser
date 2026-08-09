from os import path, makedirs
from aiohttp import web
import shutil
import filecmp 
import time
import os

from ..utils import collections_path, get_parent_path, add_uuid_to_filename, \
    config_path, get_config, git_init, run_cmd, git_remote_name



def copy_if_different(source_file, destination_file):
    """
    Copia un archivo solo si no existe en el destino o si es diferente.
    """
    # Crear las carpetas necesarias en la carpeta de destino
    makedirs(path.dirname(destination_file), exist_ok=True)

    # Solo copiar si el archivo no existe o si es diferente
    if not path.exists(destination_file) or not filecmp.cmp(source_file, destination_file, shallow=False):
        shutil.copy2(source_file, destination_file)

async def api_add_to_collections(request):
    json_data = await request.json()
    filename = json_data.get('filename')
    folder_path = json_data.get('folder_path', '')
    folder_type = json_data.get("folder_type", "outputs")
    
    if not filename:
        return web.Response(status=404, text="Filename not provided")
    
    parent_path = get_parent_path(folder_type)
    source_file_path = path.join(parent_path, folder_path, filename)
    new_filepath = path.join(collections_path(), filename)

    if not path.exists(source_file_path):
        return web.Response(status=404, text="Source file or directory not found")

    try:
        if path.isdir(source_file_path):
            # Asegurarnos de que la carpeta destino exista
            makedirs(new_filepath, exist_ok=True)

            # Recorrer todos los archivos en el directorio de origen
            for root, dirs, files in os.walk(source_file_path):
                for file in files:
                    source_file = path.join(root, file)
                    relative_path = path.relpath(source_file, source_file_path)  # Obtener la ruta relativa
                    destination_file = path.join(new_filepath, relative_path)

                    # Copiar solo si es necesario
                    copy_if_different(source_file, destination_file)

        else:
            # Es un archivo, copiar solo si es diferente
            copy_if_different(source_file_path, new_filepath)

        return web.Response(status=201, text="Files copied successfully")

    except Exception as e:
        # Manejar cualquier excepción y devolver una respuesta de error
        return web.Response(status=500, text=f"Error: {str(e)}")

# filename, content
async def api_create_new_workflow(request):
    json_data = await request.json()
    filename = json_data.get('filename')
    content = json_data.get('content')

    if not (filename and content):
        return web.Response(status=404)

    new_filepath = path.join(
        collections_path(),
        add_uuid_to_filename(filename)
    )
    with open(new_filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return web.Response(status=201)

async def api_sync_my_collections(_):
    
    if not path.exists(config_path):
        return web.Response(status=404)

    config = get_config()
    git_repo = config.get('git_repo')
    if not git_repo:
        return web.Response(status=404)

    git_init()

    cmd = 'git status -s'
    ret = run_cmd(cmd, collections_path())
    if len(ret.stdout) > 0:
        cmd = f'git add . && git commit -m "sync by comfyui-browser at {int(time.time())}"'
        ret = run_cmd(cmd, collections_path())
        if not ret.returncode == 0:
            return web.json_response(
                { 'message': "\n".join([ret.stdout, ret.stderr]) },
                status=500,
            )

    cmd = f'git fetch {git_remote_name} -v'
    ret = run_cmd(cmd, collections_path())
    if not ret.returncode == 0:
        return web.json_response(
            { 'message': "\n".join([ret.stdout, ret.stderr]) },
            status=500,
        )

    # Asegurarnos de que la rama main es la que se usa
    branch = "main"

    cmd = f'git merge {git_remote_name}/{branch}'
    ret = run_cmd(cmd, collections_path(), log_code=False)

    cmd = f'git push {git_remote_name} {branch}'
    ret = run_cmd(cmd, collections_path())
    if not ret.returncode == 0:
        return web.json_response(
            { 'message': "\n".join([ret.stdout, ret.stderr]) },
            status=500,
        )

    return web.Response(status=200)
