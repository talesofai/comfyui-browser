export interface Payload {
  workflow: Workflow;
  annotations: Annotation[];
  result: Axis[];
}

export interface Workflow {
  url: string;
}

export interface Annotation {
  axis: string;
  key: string;
  type: string;
}

export interface Axis {
  type: 'axis';
  value: string;
  children: AxisValue[];
}

export type AxisValue = Axis | ImgResult;

export interface ImgResult {
  type: 'img';
  uuid: string;
  src: string;
}

export interface AxisScore {
  type: 'axis';
  score: number;
  children?: AxisScore[];
}
