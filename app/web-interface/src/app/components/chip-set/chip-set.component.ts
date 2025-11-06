import { Component, input, output } from '@angular/core';

export type option = { id: string, text: string }

@Component({
  selector: 'app-chip-set',
  templateUrl: './chip-set.component.html',
  styleUrls: ['./chip-set.component.css'],
  standalone: true,
  imports: []
})
export class ChipSetComponent {
  selected = input.required<Array<string>>();
  options = input.required<Array<option>>();
  childEmitter = output<string>();
}
