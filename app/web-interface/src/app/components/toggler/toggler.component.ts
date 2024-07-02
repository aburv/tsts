import { Component, EventEmitter, Input, Output } from '@angular/core';

@Component({
  selector: 'app-toggler',
  templateUrl: './toggler.component.html',
  styleUrls: ['./toggler.component.css']
})
export class TogglerComponent {

  @Input() public selected!: string;
  @Input() public options!: Array<string>;
  @Output() public childEmitter = new EventEmitter();

}
