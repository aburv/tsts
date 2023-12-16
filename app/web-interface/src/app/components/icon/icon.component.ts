import { Component, Input, OnInit } from '@angular/core';
import * as icon from './icons.json';

@Component({
  selector: 'app-icon',
  templateUrl: './icon.component.html'
})
export class IconComponent implements OnInit {

  @Input()
  public name!: string;
  @Input()
  public fill!: string;
  @Input()
  public size!: number;

  viewBox = '0 0 24 24';
  iconSize = '24';
  icons: any;

  constructor() {
    this.icons = icon as any;
  }

  ngOnInit(): void {
    if (this.size) {
      this.iconSize = this.size.toString();
    }
  }
}



