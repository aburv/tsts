import { Component, input, output } from '@angular/core';

@Component({
  selector: 'app-toggler',
  templateUrl: './toggler.component.html',
  styleUrls: ['./toggler.component.css']
})
export class TogglerComponent {
  selected = input.required<string>();
  options = input.required<Array<string>>();
  childEmitter = output<string>();
}
