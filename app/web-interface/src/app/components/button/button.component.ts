import { Component, input } from '@angular/core';

import { IconComponent, Icon } from '../icon/icon.component';

export enum ButtonType {
  PRIMARY = "primary",
  PRIMARY_ICON = "primary icon",
  PRIMARY_ICON_CURVY = "primary icon curvy",
  SECONDARY = "secondary",
  SECONDARY_ICON = "secondary icon",
  SECONDARY_ICON_CURVY = "secondary icon curvy",
  DANGER = "danger",
  DANGER_ICON = "danger icon",
  DANGER_ICON_CURVY = "danger icon curvy",
  // "small" 
}

@Component({
  selector: 'app-button',
  standalone: true,
  imports: [
    IconComponent
  ],
  templateUrl: './button.component.html',
  styleUrls: ['./button.component.css']
})
export class ButtonComponent {
  type = input<ButtonType>();
  text = input<string>();
  icon = input<Icon>();
  iconColor = input<string>('var(--dark)');
  iconSize = input<number>(24);
}
