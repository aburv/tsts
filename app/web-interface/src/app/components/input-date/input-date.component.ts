import { Component, EventEmitter, Input, OnChanges, Output } from '@angular/core';
import { DateTime } from './dateTime'

@Component({
  selector: 'app-input-date',
  templateUrl: './input-date.component.html',
  styleUrls: ['./input-date.component.css']
})
export class InputDateComponent implements OnChanges {

  @Input()
  public title!: string;
  @Input()
  public value!: DateTime;
  @Input()
  public min!: DateTime;
  @Input()
  public max!: DateTime;

  @Output() public childEmitter = new EventEmitter();

  minValue!: string;
  maxValue!: string;
  valueText!: string;
  inputValue!: string;

  ngOnChanges(): void {
    if (this.min) {
      this.minValue = this.min.getISOString();
    }
    if (this.max) {
      this.maxValue = this.max.getISOString();
    }
    if (this.value) {
      this.valueText = this.value.getFormatString();
      this.inputValue = this.value.getISOString();
    }
  }

  notify(event: any): void {
    this.value.setValue(event.target.value);
    this.valueText = this.value.getFormatString();
    this.inputValue = this.value.getISOString();
    this.childEmitter.emit(event.target.value);
  }
}
