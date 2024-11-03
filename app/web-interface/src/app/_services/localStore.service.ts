import { Buffer } from 'buffer';

export class LocalDataService {
  protected key
  constructor(key: string) {
    this.key = key
  } 
  getValues(): any {
    const data = window.localStorage.getItem(this.key);
    return data !== null ? JSON.parse(Buffer.from((data), 'base64').toString('ascii')) : null;
  }

  setValues(value: any): void {
    window.localStorage.setItem(this.key, Buffer.from(JSON.stringify(value)).toString('base64'));
  }

  clearData(): void {
    window.localStorage.removeItem(this.key);
  }
}