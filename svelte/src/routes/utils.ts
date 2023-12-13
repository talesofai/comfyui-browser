import dayjs from 'dayjs';
import type Toast from './Toast.svelte';

export type FOLDER_TYPES = 'outputs' | 'collections' | 'sources';

function processFile(
  file: any,
  folderType: FOLDER_TYPES,
  comfyUrl: string,
) {
  const extname = file.name.split('.').pop().toLowerCase();
  file['fileType'] = 'json';
  if (['png', 'webp', 'jpeg', 'jpg', 'gif'].includes(extname)) {
    file['fileType'] = 'image';
  }
  if (['mp4', 'webm', 'mov', 'avi', 'mkv'].includes(extname)) {
    file['fileType'] = 'video';
  }

  file['url'] = `${comfyUrl}/browser/files/view?folder_type=${folderType}&filename=${file.name}&folder_path=${file.folder_path}`;

  const d = dayjs.unix(file.created_at);
  file['formattedDatetime'] = d.format('YYYY-MM-DD HH-mm-ss');

  if (file['bytes'] / 1024 / 1024 > 1) {
    file['formattedSize'] = (file['bytes'] / 1024 / 1024).toFixed(2) + ' MB';
  } else {
    file['formattedSize'] = Math.round(file['bytes'] / 1024) + ' KB';
  }
  return file;
}

function processDir(dir: any) {
  dir['fileType'] = 'dir';

  const newFolderPath = dir.folder_path ? `${dir.folder_path}/${dir.name}` : dir.name;
  dir['path'] = newFolderPath;

  const d = dayjs.unix(dir.created_at);
  dir['formattedDatetime'] = d.format('YYYY-MM-DD HH-mm-ss');

  dir['formattedSize'] = '0 KB';
  return dir;
}

export async function fetchFiles(
  folderType: FOLDER_TYPES,
  comfyUrl: string,
  folderPath?: string,
) {
  let url = comfyUrl + '/browser/files?folder_type=' + folderType;
  if (folderPath) {
    url = url + `&folder_path=${folderPath}&`;
  }

  const res = await fetch(url);
  const ret = await res.json();

  let files = ret.files;
  files.forEach((f: any) => {
    if (f.type === 'dir') {
      f = processDir(f);
    } else {
      f = processFile(f, folderType, comfyUrl);
    }
  });

  return files;
}

export function onScroll(showCursor: number, filesLen: number) {
  if (showCursor >= filesLen) {
    return showCursor;
  }

  const documentHeight = document.documentElement.scrollHeight;
  const scrollPosition = window.innerHeight + window.scrollY;
  if (scrollPosition >= documentHeight) {
    return showCursor + 10;
  }

  return showCursor;
}

export async function onLoadWorkflow(file: any, comfyApp: any, toast: Toast) {
  const res = await fetch(file.url);
  const blob = await res.blob();
  const fileObj = new File([blob], file.name, {
    type: res.headers.get('Content-Type') || '',
  });
  const f = comfyApp.loadGraphData.bind(comfyApp);
  comfyApp.loadGraphData = async function(graphData: any) {
    const modal = window.top?.document.getElementById('comfy-browser-dialog');
    if (modal) {
      modal.style.display = 'none';
    }
    await f(graphData);
  }
  await comfyApp.handleFile(fileObj);

  toast.show(false, 'Loaded', 'No workflow found here', 1000);
}
