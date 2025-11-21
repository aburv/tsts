export class LocalDataService {
  protected key: string;

  constructor(key: string) {
    this.key = key;
  }

  getValues(): any {
    const data = localStorage.getItem(this.key);
    if (!data) return null;

    try {
      const jsonString = decodeURIComponent(atob(data));
      return JSON.parse(jsonString);
    } catch (error) {
      console.error(`Error decoding localStorage value for key "${this.key}":`, error);
      return null;
    }
  }

  setValues(value: any): void {
    try {
      const jsonString = JSON.stringify(value);
      const encoded = btoa(encodeURIComponent(jsonString));
      localStorage.setItem(this.key, encoded);
    } catch (error) {
      console.error(`Error encoding localStorage value for key "${this.key}":`, error);
    }
  }

  clearData(): void {
    localStorage.removeItem(this.key);
  }
}
