
import {
  NavigationMenu,
  NavigationMenuContent,
  NavigationMenuIndicator,
  NavigationMenuItem,
  NavigationMenuLink,
  NavigationMenuList,
  NavigationMenuTrigger,
  navigationMenuTriggerStyle,
  NavigationMenuViewport,
} from "@/components/ui/navigation-menu";
import { Link } from "@radix-ui/react-navigation-menu";


function Header() {
  return (
    <section className="flex mx-auto p-6 bg-black justify-center">
    <NavigationMenu>
      <NavigationMenuList>
      <NavigationMenuItem >
        <ul className="flex gap-4">
          <li>
            <Link href="/docs"  >
            <NavigationMenuLink className={navigationMenuTriggerStyle()}>
              Home
            </NavigationMenuLink>
          </Link>
          </li>
          <li>
            <Link href="/docs"  >
            <NavigationMenuLink className={navigationMenuTriggerStyle()}>
              Home
            </NavigationMenuLink>
          </Link>
          </li>
        </ul>
          

      </NavigationMenuItem>
      </NavigationMenuList>
    </NavigationMenu>
  </section>
  )
}

export default Header