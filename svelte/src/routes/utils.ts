import dayjs from 'dayjs';
import type Toast from './Toast.svelte';

export async function fetchFiles(type: 'files' | 'collections', comfyUrl: string) {
  const res = await fetch(comfyUrl + '/browser/' + type);
  const ret = await res.json();

  let files = ret.files;
  files.forEach((f: any) => {
    const extname = f.name.split('.').pop().toLowerCase();
    f['fileType'] = 'json';
    if (['png', 'webp', 'jpeg', 'jpg', 'gif'].includes(extname)) {
      f['fileType'] = 'image';
    }
    if (['mp4', 'webm', 'mov', 'avi', 'mkv'].includes(extname)) {
      f['fileType'] = 'video';
    }

    if (type === 'collections') {
      f['url'] = `${comfyUrl}/browser/collections/view?filename=${f.name}`;
    } else {
      f['url'] = `${comfyUrl}/view?filename=${f.name}`;
    }

    const d = dayjs.unix(f.created_at);
    f['formattedDatetime'] = d.format('YYYY-MM-DD HH-mm-ss');

    if (f['bytes'] / 1024 / 1024 > 1) {
      f['formattedSize'] = (f['bytes'] / 1024 / 1024).toFixed(2) + ' MB';
    } else {
      f['formattedSize'] = Math.round(f['bytes'] / 1024) + ' KB';
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
