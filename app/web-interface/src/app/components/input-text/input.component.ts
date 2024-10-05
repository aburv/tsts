import { Component, input, output, HostListener, ElementRef, computed } from '@angular/core';

@Component({
  selector: 'app-input',
  templateUrl: './input.component.html',
  styleUrls: ['./input.component.css'],
})
export class InputComponent {
  static regexes: { [x: string]: RegExp } = {
    phone: /^([0-9]{10})$/,
    email: /^(([^<>()\\.,;:\s@"]+(\.[^<>()\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/,
    zip: /^[1-9][0-9]{5}$/,
    mandatory: /.+/,
    tableSeats: /^[0-9]{1}[0-9]{0,1}$/,
    currency: /^([A-Z]{3})$/,
    number: /^(?!(?:0|0\.0|0\.00)$)[+]?\d+(\.\d|\.\d[0-9])?$/,
    ip: /^([1-5]{1,3}).([1-5]{1,3}).([1-5]{1,3}).([1-5]{1,3})$/,
  };

  placeholder = input.required<string>();
  title = input.required<string>();
  value = input.required<string>();
  type = input('small')
  validator = input<string>()
  childEmitter = output<string>();

  isFocus = false;
  isValid!: boolean;
  regex = computed(() => {
    if (this.validator() !== undefined)
      return new RegExp(InputComponent.regexes[this.validator()!])
    return null
  });

  @HostListener('document:click', ['$event'])
  clickout(event: any): void {
    if (!this.eRef.nativeElement.contains(event.target)) {
      this.isFocus = false;
    }
  }

  constructor(private eRef: ElementRef) { }

  onInput(event: any): void {
    const value = event.target.value;
    this.isValid = this.regex() !== null ? this.regex()!.test(value) : true;
    if (this.isValid) {
      this.childEmitter.emit(value);
    }
  }

  getBorderColor(): string {
    if (this.isValid !== undefined && this.isValid === false) { return 'var(--danger)'; }
    return this.isFocus ? 'var(--primary)' : 'var(--less-bright)';
  }
}
