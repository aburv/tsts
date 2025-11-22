import { Component, input, output } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-toggler',
  templateUrl: './toggler.component.html',
  styleUrls: ['./toggler.component.css'],
  standalone: true,
  imports: [CommonModule]
})
export class TogglerComponent {
  selected = input.required<string>();
  options = input.required<Array<string>>();
  childEmitter = output<string>();
}
