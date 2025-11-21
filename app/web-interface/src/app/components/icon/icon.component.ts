import { Component, computed, input } from '@angular/core';
import { CommonModule } from '@angular/common';

import * as icon from './icons.json';

export enum Icon {
  SEARCH = "search",
  CROSS = "cross",
  CALENDAR = "calendar",
  PERSON = "person",
  ANDROID = "android",
  IOS = "ios"
}

@Component({
  selector: 'app-icon',
  imports:[
    CommonModule
  ],
  templateUrl: './icon.component.html'
})
export class IconComponent {
  static viewBox = '0 0 24 24';
  static icons = icon as any;

  name = input.required<Icon>();
  fill = input<string>('var(--dark)');
  size = input<number>(24);

  iconPaths = computed(() => {
    return IconComponent.icons[this.name()];
  })

  get getViewBox(): string {
    return IconComponent.viewBox;
  }
}
