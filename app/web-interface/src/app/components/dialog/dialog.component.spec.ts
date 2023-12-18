import { Component, NO_ERRORS_SCHEMA, ViewChild } from '@angular/core';
import { ComponentFixture, TestBed, async } from '@angular/core/testing';

import { DialogComponent } from './dialog.component';
import { By } from '@angular/platform-browser';

describe('DialogComponent', () => {
  let component: DialogComponent;
  let fixture: ComponentFixture<DialogComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [DialogComponent],
      schemas: [NO_ERRORS_SCHEMA],
    })
      .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(DialogComponent);
    component = fixture.componentInstance;
  });

  it('Should create', () => {
    expect(component).toBeTruthy();
  });

  it('View: Should set the dialog conent on dialog frame', () => {
    fixture.detectChanges();

    const frame = fixture.nativeElement.querySelector('.dialog-frame');
    expect(frame).not.toBe(null);

    const content = frame.querySelector('.content');
    expect(content).not.toBe(null);
  });
});