import { NO_ERRORS_SCHEMA } from '@angular/core';
import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DialogComponent } from './dialog.component';

describe('DialogComponent', () => {
  let component: DialogComponent;
  let fixture: ComponentFixture<DialogComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DialogComponent],
      schemas: [NO_ERRORS_SCHEMA],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(DialogComponent);
    component = fixture.componentInstance;
  });

  it('Should create', () => {
    expect(component).toBeTruthy();
  });

  it('View: Should set the dialog content on dialog frame', () => {
    fixture.detectChanges();

    const frame = fixture.nativeElement.querySelector('.dialog-frame');
    expect(frame).not.toBe(null);

    const content = frame.querySelector('.content');
    expect(content).not.toBe(null);
  });

  it('Should emit close when background clicked (target === currentTarget)', () => {
    const spy = spyOn((component as any).closeEmitter, 'emit');

    const ev: any = new MouseEvent('click');
    Object.defineProperty(ev, 'target', { value: ev });
    Object.defineProperty(ev, 'currentTarget', { value: ev });

    component.onBackgroundClick(ev as Event);

    expect(spy).toHaveBeenCalledWith(true);
  });

  it('Should emit close on Escape key', () => {
    const spy = spyOn(component.closeEmitter, 'emit');

    const keyEv: any = new KeyboardEvent('keydown', { key: 'Escape' });
    component.onBackgroundClick(keyEv as unknown as Event);

    expect(spy).toHaveBeenCalledWith(true);
  });

  it('Should not emit for other keys or clicks', () => {
    const spy = spyOn(component.closeEmitter, 'emit');

    const otherKey = new KeyboardEvent('keydown', { key: 'Enter' });
    component.onBackgroundClick(otherKey as unknown as Event);

    const clickEv: any = { target: {}, currentTarget: {} };
    clickEv.target = {};
    component.onBackgroundClick(clickEv as Event);

    expect(spy).not.toHaveBeenCalled();
  });
});