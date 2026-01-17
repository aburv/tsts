import { CommonModule } from '@angular/common';
import { Component, Input, output, TemplateRef } from '@angular/core';

@Component({
  selector: 'app-dialog',
  standalone: true,
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

  onBackgroundClick(event: Event): void {
    if (event instanceof MouseEvent) {
      if (event.target === event.currentTarget) {
        this.closeEmitter.emit(true);
      }
    } else if (event instanceof KeyboardEvent) {
      if (event.key === 'Escape') {
        this.closeEmitter.emit(true);
      }
    }
  }
}
