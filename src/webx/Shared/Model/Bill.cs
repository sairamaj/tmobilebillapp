using System;

namespace web.Shared.Model
{
    internal class Bill
    {
        public string Type { get; set; }
        public decimal Total { get; set; }
        public decimal PerLine { get; set; }

                // bill date will be of "Summary_Apr2020" format.
        public string YearMonth => this.Type.Substring("Summary_".Length);
        public DateTime Date
        {
            get
            {
                if (DateTime.TryParse(this.YearMonth, out var val))
                {
                    return val;
                }

                return DateTime.MinValue;
            }
        }

        public string DateAsString => this.Date.ToString("MMM yyyy");
        public string PdfDownloadLink {get; set;}
    }
}