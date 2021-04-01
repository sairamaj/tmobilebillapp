using Markdig;

namespace SelfService.Shared
{
    public class HomePageResource
    {
        public int Order {get; set;}
        public string Title { get; set; }
        public string Info { get; set; }

        public string InfoAsMarkdown
        {
            get
            {
                if (string.IsNullOrWhiteSpace(this.Info))
                {
                    return string.Empty;
                }
                return Markdown.ToHtml(this.Info);
            }
        }

    }
}