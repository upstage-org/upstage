export interface StageGraph {
  stageList: StageList;
}

export interface StageList {
  edges: Edge[];
  __typename: string;
}

export interface Edge {
  node: Node;
  __typename: EdgeTypename;
}

export enum EdgeTypename {
  StageEdge = "StageEdge",
}

export interface Node {
  id: string;
  name: string;
  __typename: NodeTypename;
}

export enum NodeTypename {
  Stage = "Stage",
}
