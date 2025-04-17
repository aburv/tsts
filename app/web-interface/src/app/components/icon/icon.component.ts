import { Component, computed, input } from '@angular/core';
import * as icon from './icons.json';

@Component({
  selector: 'app-icon',
  templateUrl: './icon.component.html'
})
export class IconComponent {
  static viewBox = '0 0 24 24';
  static icons = icon as any;

  name = input.required<string>();
  fill = input<string>('var(--dark)');
  size = input<number>(24);

  iconPaths = computed(() => {
    return IconComponent.icons[this.name()];
  })

  get getViewBox(): string {
    return IconComponent.viewBox;
  }
}
