import { CommonModule } from '@angular/common';
import { Component, Input, output, TemplateRef } from '@angular/core';

@Component({
  selector: 'app-dialog',
  imports: [
    CommonModule
  ],
  templateUrl: 'dialog.component.html',
  styleUrls: ['dialog.component.css'],
})
export class DialogComponent {
  @Input()
  content!: TemplateRef<any>;

  closeEmitter = output<boolean>();

  onBackgroundClick(event: MouseEvent): void {
    if (event.target === event.currentTarget) {
      this.closeEmitter.emit(true);
    }
  }
}
