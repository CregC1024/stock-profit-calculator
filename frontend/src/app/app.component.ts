import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { StockService } from './services/stock.service';
import { StockCalculationResponse } from './models/stock.model';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  private fb = inject(FormBuilder);
  private stockService = inject(StockService);

  calcForm!: FormGroup;
  result: StockCalculationResponse | null = null;
  loading = false;
  errorMessage = '';

  presets = [
    {
      name: '📈 Profitable Trade',
      shares: 100,
      purchase_price: 50.0,
      purchase_commission: 10.0,
      sale_price: 75.0,
      sale_commission: 10.0
    },
    {
      name: '📉 Loss Trade',
      shares: 100,
      purchase_price: 100.0,
      purchase_commission: 15.0,
      sale_price: 82.5,
      sale_commission: 15.0
    },
    {
      name: '⚖️ Break-Even Trade',
      shares: 500,
      purchase_price: 20.0,
      purchase_commission: 9.95,
      sale_price: 20.04,
      sale_commission: 10.05
    },
    {
      name: '🚀 High Volume Tech Stock',
      shares: 1000,
      purchase_price: 150.0,
      purchase_commission: 0.0,
      sale_price: 165.25,
      sale_commission: 0.0
    }
  ];

  ngOnInit(): void {
    this.calcForm = this.fb.group({
      shares: [100, [Validators.required, Validators.min(0.0001)]],
      purchase_price: [50.0, [Validators.required, Validators.min(0)]],
      purchase_commission: [10.0, [Validators.required, Validators.min(0)]],
      sale_price: [75.0, [Validators.required, Validators.min(0)]],
      sale_commission: [10.0, [Validators.required, Validators.min(0)]]
    });

    // Automatically calculate initial values
    this.onCalculate();
  }

  onCalculate(): void {
    if (this.calcForm.invalid) {
      this.errorMessage = 'Please enter valid values for all input fields.';
      return;
    }

    this.errorMessage = '';
    this.loading = true;
    const formValues = this.calcForm.value;

    this.stockService.calculate({
      shares: Number(formValues.shares),
      purchase_price: Number(formValues.purchase_price),
      purchase_commission: Number(formValues.purchase_commission),
      sale_price: Number(formValues.sale_price),
      sale_commission: Number(formValues.sale_commission)
    }).subscribe({
      next: (res) => {
        this.result = res;
        this.loading = false;
      },
      error: (err) => {
        this.errorMessage = 'Failed to process calculation request.';
        this.loading = false;
      }
    });
  }

  applyPreset(preset: typeof this.presets[0]): void {
    this.calcForm.patchValue({
      shares: preset.shares,
      purchase_price: preset.purchase_price,
      purchase_commission: preset.purchase_commission,
      sale_price: preset.sale_price,
      sale_commission: preset.sale_commission
    });
    this.onCalculate();
  }

  resetForm(): void {
    this.calcForm.reset({
      shares: 100,
      purchase_price: 0,
      purchase_commission: 0,
      sale_price: 0,
      sale_commission: 0
    });
    this.result = null;
    this.errorMessage = '';
  }
}
