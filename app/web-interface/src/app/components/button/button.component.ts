import { Component, input } from '@angular/core';

@Component({
  selector: 'app-button',
  templateUrl: './button.component.html',
  styleUrls: ['./button.component.css']
})
export class ButtonComponent {
  type = input<string>();
  text = input<string>();
  icon = input<string>();
  iconColor = input<string>('var(--dark)');
  iconSize = input<number>(24);
}
