import { Component, computed, input, output } from '@angular/core';

import { DateTime } from './dateTime'
import { Icon, IconComponent } from '../icon/icon.component';

@Component({
  selector: 'app-input-date',
  standalone: true,
  imports: [
    IconComponent
  ],
  templateUrl: './input-date.component.html',
  styleUrls: ['./input-date.component.css']
})
export class InputDateComponent {
  readonly Icon = Icon
  title = input<string>();
  value = input<DateTime>();
  min = input<DateTime>();
  max = input<DateTime>();

  childEmitter = output<string>();

  minValue = computed(() => {
    if (this.min() !== undefined) {
      return this.min()!.getISOString();
    }
    return null
  });
  maxValue = computed(() => {
    if (this.max() !== undefined) {
      return this.max()!.getISOString();
    }
    return null
  });

  inputValue = computed(() => {
    if (this.value() !== undefined) {
      return this.value()!.getISOString();
    }
    return null
  });

  valueText = computed(() => {
    if (this.value() !== undefined) {
      return this.value()!.getFormatString();
    }
    return null
  });

  notify(event: any): void {
    this.value()!.setValue(event.target.value);
    this.childEmitter.emit(event.target.value);
  }
}
