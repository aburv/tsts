import { Component, EventEmitter, Input, Output } from '@angular/core';

@Component({
  selector: 'app-chip-set',
  templateUrl: './chip-set.component.html',
  styleUrls: ['./chip-set.component.css']
})
export class ChipSetComponent {

  @Input()
  public selected!: Array<string>;
  @Input() 
  public options!: Array<{id: string, text: string}>;
  @Output() 
  public childEmitter = new EventEmitter();

}
