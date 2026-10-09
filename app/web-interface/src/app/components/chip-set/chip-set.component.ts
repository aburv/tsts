import { Component, input, output } from '@angular/core';

export interface option { id: string, text: string }

@Component({
  selector: 'app-chip-set',
  templateUrl: './chip-set.component.html',
  styleUrls: ['./chip-set.component.css'],
  standalone: true,
  imports: []
})
export class ChipSetComponent {
  selected = input.required<string[]>();
  options = input.required<option[]>();
  childEmitter = output<string>();
}
