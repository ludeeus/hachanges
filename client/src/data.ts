export interface Change {
  homeassistant: number;
  title: string;
  description: string;
  pull_request: number;
  pull: number;
  integration: string;
  component: string;
  doclink: string;
  prlink: string;
}

export const getChanges = async (version: string) => {
  const response = await fetch(`/${version}/json`);
  return await response.json();
};
